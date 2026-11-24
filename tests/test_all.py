#!/usr/bin/env python3
"""Offline tests for build-tools. Run: python3 -I tests/test_all.py"""
import json, os, re, shutil, subprocess, sys, tempfile, zipfile, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "build-tools")
S = os.path.join(SK, "scripts")
SH = shutil.which("dash") or shutil.which("sh")
fails = []


def run(args, env=None):
    e = dict(os.environ); e.update(env or {})
    return subprocess.run(args, capture_output=True, text=True, env=e)


def py(script, *a):
    return run([sys.executable, "-I", os.path.join(S, script)] + list(a))


def check(name, cond, extra=""):
    print(("ok   " if cond else "FAIL ") + name + (" " + extra if (extra and not cond) else ""))
    if not cond:
        fails.append(name)


tmp = tempfile.mkdtemp()
try:
    for kind in ("basic", "service", "props", "canary"):
        mid = "t_" + kind
        r = py("new_module.py", "--kind", kind, "--id", mid, "--name", "T", "--desc", "d", "--out", tmp)
        check(kind + " scaffold", r.returncode == 0, r.stderr)
        check(kind + " no overwrite", py("new_module.py", "--kind", kind, "--id", mid, "--name", "T", "--out", tmp).returncode == 2)
        md = os.path.join(tmp, mid)
        r = py("lint_module.py", md)
        check(kind + " lint", "STATUS: PASS_STRUCTURAL" in r.stdout and "DEVICE: NOT_TESTED" in r.stdout, r.stdout)
        out1, out2 = os.path.join(tmp, "o1"), os.path.join(tmp, "o2")
        b1 = py("build_zip.py", md, "--out", out1); b2 = py("build_zip.py", md, "--out", out2)
        check(kind + " build", b1.returncode == 0, b1.stdout)
        z1 = os.path.join(out1, mid + "-v1.0.0.zip"); z2 = os.path.join(out2, mid + "-v1.0.0.zip")
        h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
        check(kind + " deterministic", h(z1) == h(z2))
        check(kind + " rebuild refuses overwrite", py("build_zip.py", md, "--out", out1).returncode == 2)
        check(kind + " zip lints", "PASS_STRUCTURAL" in py("lint_module.py", z1).stdout)
        # simulation
        sim = os.path.join(tmp, "sim_" + kind)
        os.makedirs(sim + "/int"); os.makedirs(sim + "/docs")
        env = {"DBG_FORCE_READY": "1", "BT_ONCE": "1", "DBG_INT_DIR": sim + "/int", "DBG_DOCS_DIR": sim + "/docs"}
        for sc in ("post-fs-data.sh", "service.sh"):
            run([SH, os.path.join(md, sc)], env)
        log = os.path.join(sim, "docs", mid + "-debug.log")
        check(kind + " log copied", os.path.isfile(log))
        if os.path.isfile(log):
            p = py("parse_report.py", log, "--manifest", os.path.join(out1, mid + "-v1.0.0.manifest.json"))
            want = "STATUS: FAIL" if kind == "props" else "STATUS: PASS_SIMULATED"  # props cannot apply in sandbox
            check(kind + " report " + want, want in p.stdout, p.stdout)
            check(kind + " never PASS_REAL offline", "PASS_REAL" not in p.stdout)
    # guard
    md = os.path.join(tmp, "t_basic"); g = os.path.join(tmp, "g"); os.makedirs(g + "/int")
    for _ in range(4):
        run([SH, os.path.join(md, "post-fs-data.sh")], {"DBG_FORCE_READY": "1", "DBG_INT_DIR": g + "/int", "DBG_DOCS_DIR": g + "/d"})
    check("guard creates disable", os.path.exists(os.path.join(md, "disable")))
    os.remove(os.path.join(md, "disable"))
    # mutations
    def mutate(name, fn, rule):
        d = os.path.join(tmp, "m_" + name); shutil.copytree(os.path.join(tmp, "t_basic"), d)
        fn(d)
        r = py("lint_module.py", d)
        check("mutation " + name, rule in r.stdout and "STATUS: FAIL" in r.stdout, r.stdout)
    def edit(f, fn):
        def g2(d):
            p = os.path.join(d, f); s = open(p).read(); open(p, "w", newline="").write(fn(s))
        return g2
    mutate("crlf", edit("service.sh", lambda s: s.replace("\n", "\r\n")), "LM020")
    mutate("setprop", edit("post-fs-data.sh", lambda s: s + "\nsetprop a b\n"), "LM024")
    mutate("exit_customize", edit("customize.sh", lambda s: s + "\nexit 0\n"), "LM028")
    mutate("badid", edit("module.prop", lambda s: s.replace("id=t_basic", "id=1bad")), "LM003")
    mutate("no_dbg", lambda d: os.remove(os.path.join(d, "dbg.sh")), "LM030")
    mutate("install_sh", lambda d: open(os.path.join(d, "install.sh"), "w").write("x"), "LM011")
    mutate("syntax", edit("service.sh", lambda s: s + "\nif then fi (\n"), "LM022")
    mutate("rm", edit("service.sh", lambda s: s + "\nrm -rf /data\n"), "LM025")
    mutate("vc", edit("module.prop", lambda s: s.replace("versionCode=1", "versionCode=x")), "LM004")
    # status logic
    bad = os.path.join(tmp, "bad.log"); open(bad, "w").write("2026-01-01 00:00:00 ERROR [service] CHECK x FAIL\n")
    check("report FAIL", "STATUS: FAIL" in py("parse_report.py", bad).stdout)
    empty = os.path.join(tmp, "e.log"); open(empty, "w").write("nothing\n")
    check("report NOT_TESTED", "STATUS: NOT_TESTED" in py("parse_report.py", empty).stdout)
    # skill spec
    t = open(os.path.join(SK, "SKILL.md")).read()
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---", t)
    check("skill name", m and m.group(1) == "build-tools" == os.path.basename(SK))
    check("skill description <=1024", m and len(m.group(2)) <= 1024)
    check("skill <500 lines", t.count("\n") < 500)
    check("evals >=12", len(json.load(open(os.path.join(SK, "evals/evals.json")))["evals"]) >= 12)
    ub = open(os.path.join(SK, "assets/templates/_common/META-INF/com/google/android/update-binary")).read()
    check("update-binary official", "install_module" in ub)
    # installer
    sk = os.path.join(tmp, "skills")
    e = {"CLAUDE_SKILLS_DIR": sk, "BT_SOURCE_DIR": ROOT}
    check("install sh -n", run([SH, "-n", os.path.join(ROOT, "install.sh")]).returncode == 0)
    check("install --check", "OK" in run([SH, os.path.join(ROOT, "install.sh"), "--check"], e).stdout and not os.path.exists(sk + "/build-tools"))
    check("install", run([SH, os.path.join(ROOT, "install.sh")], e).returncode == 0 and os.path.isfile(sk + "/build-tools/SKILL.md"))
    r = run([SH, os.path.join(ROOT, "install.sh")], e)
    check("install backs up", "Backed up" in r.stdout and any(".bak." in x for x in os.listdir(sk)))
    check("uninstall", run([SH, os.path.join(ROOT, "install.sh"), "--uninstall"], e).returncode == 0 and not os.path.exists(sk + "/build-tools"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print("FAILED: %d" % len(fails) if fails else "ALL TESTS PASSED")
sys.exit(1 if fails else 0)

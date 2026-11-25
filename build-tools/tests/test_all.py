#!/usr/bin/env python3
"""test_all.py - offline verification for the build-tools skill itself.

Scaffolds every template kind (plus a --webui variant), lints them, simulates
the canary and service stages under dash, builds a zip, runs parse_report on
the simulation log, and checks that lint catches known-bad patterns (wm in a
service, external URL in a WebUI, thermal reads without a range filter).

Usage: python3 -I tests/test_all.py
Exit 0 = all passed. Needs dash or sh. No phone, no network.
Kid note: this checks the skill's own tools before they ever touch a phone.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
PY = [sys.executable, "-I"]
FAILURES = []


def run(args, env=None, cwd=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(args, capture_output=True, text=True, env=e, cwd=cwd)


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" :: " + detail.strip()[:200]) if (detail and not ok) else ""))
    if not ok:
        FAILURES.append(name)


def scaffold(tmp, kind, mid, webui=False):
    args = PY + [os.path.join(SCRIPTS, "new_module.py"), "--kind", kind, "--id", mid,
                 "--name", "Test " + kind, "--desc", "test_all scaffold", "--out", os.path.join(tmp, kind + mid)]
    if webui:
        args.append("--webui")
    r = run(args)
    dest = os.path.join(tmp, kind + mid, mid)
    check("scaffold %s%s" % (kind, "+webui" if webui else ""), r.returncode == 0 and os.path.isdir(dest), r.stdout + r.stderr)
    return dest


def lint(dest):
    return run(PY + [os.path.join(SCRIPTS, "lint_module.py"), dest])


def main():
    sh = shutil.which("dash") or shutil.which("sh")
    check("dash/sh available", sh is not None)
    if not sh:
        return 1
    tmp = tempfile.mkdtemp(prefix="build-tools-test-")
    try:
        dests = {}
        for kind in ("basic", "service", "props", "canary"):
            dests[kind] = scaffold(tmp, kind, "test_" + kind)
            r = lint(dests[kind])
            check("lint %s PASS_STRUCTURAL" % kind, "STATUS: PASS_STRUCTURAL" in r.stdout, r.stdout + r.stderr)
        webui_dest = scaffold(tmp, "service", "test_webui", webui=True)
        check("webui starter present", os.path.isfile(os.path.join(webui_dest, "webroot", "index.html")))
        r = lint(webui_dest)
        check("lint webui variant PASS_STRUCTURAL", "STATUS: PASS_STRUCTURAL" in r.stdout, r.stdout + r.stderr)

        # Lint must catch known-bad patterns (log-derived rules).
        bad = os.path.join(tmp, "bad")
        shutil.copytree(webui_dest, bad)
        with open(os.path.join(bad, "service.sh"), "a") as fh:
            fh.write("\nwm size\ncat /sys/class/thermal/thermal_zone0/temp\n")
        with open(os.path.join(bad, "webroot", "index.html"), "a") as fh:
            fh.write('<script src="https://example.com/x.js"></script>\n')
        r = lint(bad)
        check("lint catches wm (LM035)", "LM035" in r.stdout, r.stdout)
        check("lint catches external URL (LM036)", "LM036" in r.stdout, r.stdout)
        check("lint catches unfiltered thermal (LM038)", "LM038" in r.stdout, r.stdout)

        # Simulate canary + service stages under dash.
        for kind in ("canary", "service"):
            dest = dests[kind]
            logs = os.path.join(tmp, kind + "-logs")
            docs = os.path.join(tmp, kind + "-docs")
            env = {"DBG_INT_DIR": logs, "DBG_DOCS_DIR": docs, "DBG_FORCE_READY": "1", "BT_ONCE": "1"}
            ok = True
            detail = ""
            for stage in ("post-fs-data.sh", "service.sh"):
                p = os.path.join(dest, stage)
                if os.path.isfile(p):
                    r = run([sh, p], env=env, cwd=dest)
                    if r.returncode != 0:
                        ok = False
                        detail = stage + ": " + r.stdout + r.stderr
            check("dash sim %s" % kind, ok, detail)
            log = os.path.join(logs, "test_%s-debug.log" % kind)
            check("sim log exists %s" % kind, os.path.isfile(log))
            if os.path.isfile(log):
                out = os.path.join(tmp, kind + "-out.zip")
                r = run(PY + [os.path.join(SCRIPTS, "build_zip.py"), dest, "--out", out])
                check("build zip %s" % kind, r.returncode == 0 and "STATUS: PASS_STRUCTURAL" in r.stdout, r.stdout + r.stderr)
                manifest = os.path.join(out, "test_%s-v1.0.0.manifest.json" % kind)
                r = run(PY + [os.path.join(SCRIPTS, "parse_report.py"), log, "--manifest", manifest])
                check("parse_report sim %s = PASS_SIMULATED" % kind, "STATUS: PASS_SIMULATED" in r.stdout, r.stdout + r.stderr)
                check("parse_report AVC module split %s" % kind, "(module " in r.stdout, r.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT: %s (%d failures)" % ("PASS" if not FAILURES else "FAIL", len(FAILURES)))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())

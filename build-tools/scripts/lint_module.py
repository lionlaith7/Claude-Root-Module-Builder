#!/usr/bin/env python3
"""lint_module.py - check a module folder or .zip against known Magisk/KernelSU rules.

Usage: python3 -I lint_module.py PATH [--json] [--skip-log-policy]
Prints findings, then 'STATUS: PASS_STRUCTURAL' or 'STATUS: FAIL' and 'DEVICE: NOT_TESTED'.
PASS_STRUCTURAL only means the files look right. It never means it works on a phone.
Kid note: this is a spell-checker for modules; it finds mistakes before the phone does.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

ID_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9._-]+$")
BOOT_SCRIPTS = ("post-fs-data.sh", "service.sh")
JUNK = (".DS_Store", "Thumbs.db", ".gitignore")
SECRET_RE = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


def load(path):
    """Return dict relpath -> bytes, and info about wrapping."""
    files = {}
    wrapped = False
    if os.path.isdir(path):
        for root, _d, fs in os.walk(path):
            for f in fs:
                p = os.path.join(root, f)
                with open(p, "rb") as fh:
                    files[os.path.relpath(p, path).replace(os.sep, "/")] = fh.read()
    else:
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if not n.endswith("/"):
                    files[n] = z.read(n)
        tops = {n.split("/")[0] for n in files}
        if "module.prop" not in files and len(tops) == 1 and any(n.startswith(next(iter(tops)) + "/module.prop") for n in files):
            wrapped = True
    return files, wrapped


def parse_prop(data):
    d = {}
    for line in data.decode("utf-8", "replace").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def sh_syntax(name, data):
    sh = shutil.which("dash") or shutil.which("sh")
    if not sh:
        return None
    r = subprocess.run([sh, "-n"], input=data, capture_output=True)
    return None if r.returncode == 0 else r.stderr.decode("utf-8", "replace").strip()


def lint(path, skip_log_policy=False):
    F = []  # (rule, level, message)

    def add(rule, level, msg):
        F.append({"rule": rule, "level": level, "message": msg})

    files, wrapped = load(path)
    if wrapped:
        add("LM010", "ERROR", "zip is wrapped in a folder; module.prop must be at the zip root")
    if "module.prop" not in files:
        add("LM001", "ERROR", "module.prop missing")
        return F
    prop = parse_prop(files["module.prop"])
    for k in ("id", "name", "version", "versionCode", "author", "description"):
        if not prop.get(k):
            add("LM002", "ERROR", "module.prop field missing or empty: " + k)
    mid = prop.get("id", "")
    if mid and not ID_RE.match(mid):
        add("LM003", "ERROR", "id '%s' does not match ^[a-zA-Z][a-zA-Z0-9._-]+$" % mid)
    if prop.get("versionCode") and not prop["versionCode"].isdigit():
        add("LM004", "ERROR", "versionCode must be an integer")
    if "install.sh" in files:
        add("LM011", "ERROR", "install.sh must not be in the module zip (legacy format)")
    ub = files.get("META-INF/com/google/android/update-binary")
    us = files.get("META-INF/com/google/android/updater-script")
    if ub is None:
        add("LM012", "ERROR", "META-INF/com/google/android/update-binary missing")
    elif b"install_module" not in ub:
        add("LM013", "ERROR", "update-binary is not the official module_installer.sh (no install_module)")
    if us is None:
        add("LM014", "ERROR", "updater-script missing")
    elif us.strip() != b"#MAGISK":
        add("LM015", "ERROR", "updater-script must contain only #MAGISK")
    for n in files:
        if os.path.basename(n) in JUNK or "__MACOSX" in n:
            add("LM016", "WARN", "junk file: " + n)
    for n, data in sorted(files.items()):
        is_text = n.endswith((".sh", ".prop", ".rule", ".list")) or os.path.basename(n) in ("update-binary", "updater-script")
        if not is_text:
            continue
        if b"\r\n" in data:
            add("LM020", "ERROR", "CRLF line endings (must be LF): " + n)
        if SECRET_RE.search(data.decode("utf-8", "replace")):
            add("LM021", "ERROR", "possible secret/token in " + n)
        if n.endswith(".sh") or os.path.basename(n) == "update-binary":
            err = sh_syntax(n, data)
            if err:
                add("LM022", "ERROR", "shell syntax error in %s: %s" % (n, err.splitlines()[0] if err else ""))
        if n.endswith(".sh") and n != "META-INF/com/google/android/update-binary":
            text = data.decode("utf-8", "replace")
            body = [l for l in text.splitlines() if not l.strip().startswith("#") and "bt_try_shell" not in l]
            joined = "\n".join(body)
            if re.search(r"\[\[|\bfunction\s+\w+\s*\(|<<<|\bsource\s", joined):
                add("LM023", "WARN", "possible bashism ([[ ]], function keyword, <<<, source) in " + n)
            if os.path.basename(n) == "post-fs-data.sh" and re.search(r"(^|[;&|\s])setprop\s", joined):
                add("LM024", "ERROR", "setprop in post-fs-data.sh can deadlock boot; use resetprop -n")
            if re.search(r"rm\s+-rf?\s+(/|/data|/system|/sdcard|\$\{?[A-Za-z_]+\}?/?\s*$)", joined, re.M):
                add("LM025", "ERROR", "dangerous rm -rf target in " + n)
            if re.search(r"(>|>>|\bcp\b[^\n]*|\bmv\b[^\n]*)\s+/system/", joined):
                add("LM026", "ERROR", "writes into /system (use system/ folder in the module): " + n)
            if mid and re.search(r"/data/adb/modules/" + re.escape(mid) + r"(/|\b)", joined):
                add("LM027", "WARN", "hardcoded own module path in %s; use MODDIR=${0%%/*}" % n)
            if re.search(r"(^|[;&|\s])wm\s+(size|density|overscan|dismiss-keyguard)\b", joined):
                add("LM035", "WARN", "wm command in %s: wm fails from a module service context (T3 2026-11-25); use dumpsys display or props" % n)
            if "thermal_zone" in joined and not re.search(r"(-gt|-ge|-lt|-le|>|<)\s*120\b|120000|plausible|range|filter", joined):
                add("LM038", "WARN", "thermal_zone reads in %s without a plausible-range filter; some zones are levels/voltages, not temperatures (see patterns.md)" % n)
    cz = files.get("customize.sh")
    if cz is not None:
        lines = [l.strip() for l in cz.decode("utf-8", "replace").splitlines() if l.strip() and not l.strip().startswith("#")]
        if any(re.match(r"exit(\s|$)", l) for l in lines):
            add("LM028", "ERROR", "customize.sh is sourced: use abort, never exit")
    # WebUI rules (references/webui.md): self-contained, no external URLs, small.
    for n, data in sorted(files.items()):
        if n.startswith("webroot/") and n.endswith((".html", ".htm")):
            html = data.decode("utf-8", "replace")
            if re.search(r"https?://|src\s*=\s*[\"']//|href\s*=\s*[\"']//", html):
                add("LM036", "ERROR", "external URL in %s: WebUI must be self-contained (no CDN, fonts, images)" % n)
            if len(data) > 200 * 1024:
                add("LM037", "WARN", "%s is %d KB: keep WebUI index.html under ~200 KB" % (n, len(data) // 1024))
            if "innerHTML" in html:
                add("LM039", "WARN", "innerHTML in %s: put device strings in the DOM with textContent only" % n)
            if "ksu.exec" in html and "fetch(" not in html:
                add("LM040", "WARN", "ksu.exec in %s without a fetch fallback: a detected-but-silent bridge hangs the UI; always fall back to service-written JSON (HotMod v1.0 lesson, real device 2026-11-25)" % n)
    if not skip_log_policy:
        if "dbg.sh" not in files:
            add("LM030", "ERROR", "dbg.sh missing (every module must write the debug log)")
        else:
            d = files["dbg.sh"].decode("utf-8", "replace")
            if "Documents" not in d:
                add("LM031", "ERROR", "dbg.sh does not write to Documents")
            m = re.search(r'DBG_ID="?([^"\s]+)"?', "\n".join(files.get(s, b"").decode("utf-8", "replace") for s in BOOT_SCRIPTS + ("customize.sh",)))
        for s in BOOT_SCRIPTS:
            if s in files:
                t = files[s].decode("utf-8", "replace")
                if "dbg.sh" not in t:
                    add("LM032", "ERROR", "%s does not source dbg.sh" % s)
                m = re.search(r'^DBG_ID="?([^"\s]+)"?', t, re.M)
                if m and mid and m.group(1) != mid:
                    add("LM033", "ERROR", "DBG_ID in %s is '%s' but module id is '%s'" % (s, m.group(1), mid))
        if not any(s in files for s in BOOT_SCRIPTS):
            add("LM034", "WARN", "no boot script (post-fs-data.sh/service.sh): the module never logs at boot")
    return F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip-log-policy", action="store_true")
    a = ap.parse_args()
    try:
        F = lint(a.path, a.skip_log_policy)
    except (OSError, zipfile.BadZipFile) as e:
        print("STATUS: FAIL\nERROR: cannot read %s: %s" % (a.path, e))
        return 2
    errors = [f for f in F if f["level"] == "ERROR"]
    status = "FAIL" if errors else "PASS_STRUCTURAL"
    if a.json:
        print(json.dumps({"status": status, "device": "NOT_TESTED", "findings": F}, indent=2))
    else:
        for f in F:
            print("%s %s %s" % (f["level"], f["rule"], f["message"]))
        print("STATUS: " + status)
        print("DEVICE: NOT_TESTED")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

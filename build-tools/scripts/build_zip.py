#!/usr/bin/env python3
"""build_zip.py - lint, then build a deterministic module zip plus a manifest with sha256 hashes.

Usage: python3 -I build_zip.py MODULE_DIR [--out DIR] [--force] [--skip-log-policy]
Output: <id>-<version>.zip and <id>-<version>.manifest.json
Same input gives the same zip bytes (fixed timestamps, sorted entries).
Kid note: this packs the module into a zip the same way every time and writes a fingerprint list.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_module  # noqa: E402

FIXED = (2020, 1, 1, 0, 0, 0)
EXEC_NAMES = {"update-binary"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("module_dir")
    ap.add_argument("--out", default=".")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-log-policy", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.module_dir):
        print("ERROR: not a folder: " + a.module_dir)
        return 2
    findings = lint_module.lint(a.module_dir, a.skip_log_policy)
    for f in findings:
        print("%s %s %s" % (f["level"], f["rule"], f["message"]))
    if any(f["level"] == "ERROR" for f in findings):
        print("STATUS: FAIL (lint errors; no zip built)")
        return 1
    files, _ = lint_module.load(a.module_dir)
    prop = lint_module.parse_prop(files["module.prop"])
    base = "%s-%s" % (prop["id"], re.sub(r"[^A-Za-z0-9._-]", "_", prop["version"]))
    os.makedirs(a.out, exist_ok=True)
    zpath = os.path.join(a.out, base + ".zip")
    mpath = os.path.join(a.out, base + ".manifest.json")
    if (os.path.exists(zpath) or os.path.exists(mpath)) and not a.force:
        print("ERROR: %s exists; use --force to replace" % zpath)
        return 2
    entries = {}
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            if name.endswith(".log"):
                continue
            data = files[name]
            zi = zipfile.ZipInfo(name, FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if (name.endswith(".sh") or os.path.basename(name) in EXEC_NAMES) else 0o644
            zi.external_attr = (0o100000 | mode) << 16
            zi.create_system = 3
            z.writestr(zi, data)
            entries[name] = sha(data)
    with open(zpath, "rb") as fh:
        zhash = sha(fh.read())
    manifest = {
        "id": prop["id"],
        "version": prop["version"],
        "versionCode": prop["versionCode"],
        "zip": os.path.basename(zpath),
        "zip_sha256": zhash,
        "files": entries,
    }
    with open(mpath, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    again = lint_module.lint(zpath, a.skip_log_policy)
    if any(f["level"] == "ERROR" for f in again):
        print("STATUS: FAIL (built zip does not lint)")
        return 1
    print("BUILT %s" % zpath)
    print("SHA256 %s" % zhash)
    print("MANIFEST %s" % mpath)
    print("STATUS: PASS_STRUCTURAL")
    print("DEVICE: NOT_TESTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

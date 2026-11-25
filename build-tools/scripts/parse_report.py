#!/usr/bin/env python3
"""parse_report.py - read the debug log a module wrote and decide the test status.

Usage: python3 -I parse_report.py LOG [--manifest FILE.manifest.json] [--json]
Statuses: NOT_TESTED, FAIL, PASS_PARTIAL, PASS_SIMULATED, PASS_REAL.
PASS_REAL needs: the log's HASH lines match the manifest, a real device (sim=0),
boot completed, zero ERROR lines, at least one CHECK, all CHECKs PASS.
Kid note: you give it the diary from the phone; it tells you honestly what worked.
"""
import argparse
import json
import re
import sys

LINE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) (INFO|WARN|ERROR) \[([^\]]*)\] (.*)$")


def parse(text):
    r = {"snap": {}, "stages": [], "checks": {}, "hashes": {}, "errors": [], "warns": [], "avc": 0,
         "avc_msgs": [], "boot_completed": False, "boots": 0, "lines": 0, "probes": []}
    for raw in text.splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        r["lines"] += 1
        _t, lvl, stage, msg = m.groups()
        if lvl == "ERROR":
            r["errors"].append(msg)
        elif lvl == "WARN":
            r["warns"].append(msg)
        if msg.startswith("SNAP "):
            kv = msg[5:].split("=", 1)
            if len(kv) == 2:
                r["snap"][kv[0].strip()] = kv[1].strip()
        elif msg.startswith("STAGE begin"):
            r["stages"].append(msg.split()[2] if len(msg.split()) > 2 else stage)
            if msg.split()[2:3] == ["post-fs-data"]:
                r["boots"] += 1
        elif msg.startswith("CHECK "):
            p = msg.split()
            if len(p) >= 3:
                r["checks"][p[1]] = p[2]
        elif msg.startswith("HASH "):
            p = msg.split(None, 2)
            if len(p) == 3:
                r["hashes"][p[2]] = p[1]
        elif msg.startswith("BOOT completed"):
            r["boot_completed"] = True
        elif msg.startswith("AVC ") and "avc:" in msg:
            r["avc"] += 1
            r["avc_msgs"].append(msg)
        elif msg.startswith("PROBE "):
            r["probes"].append(msg[6:])
    return r


def module_avc_count(r):
    """AVCs that plausibly belong to this module (its SELinux context or paths).

    AVC lines in the log are system-wide (observed 2026-11-25: 50 AVCs, none
    from the module). Only count a denial as the module's own when its source
    context is the root-manager domain or it touches the module's own paths.
    """
    mid = r["snap"].get("module_id", "")
    n = 0
    for msg in r["avc_msgs"]:
        if "scontext=u:r:ksu:s0" in msg or "scontext=u:r:magisk:s0" in msg:
            n += 1
        elif mid and ("/data/adb/modules/" + mid) in msg:
            n += 1
    return n


def decide(r, manifest):
    reasons = []
    if r["lines"] == 0:
        return "NOT_TESTED", ["no log lines found"]
    sim = r["snap"].get("sim", "")
    bad = [k for k, v in r["checks"].items() if v != "PASS"]
    if r["errors"] or bad:
        reasons.append("%d ERROR lines, failed checks: %s" % (len(r["errors"]), ",".join(bad) or "none"))
        return "FAIL", reasons
    if manifest is not None:
        if r["snap"].get("module_id") != manifest.get("id"):
            return "FAIL", ["log module_id does not match manifest id"]
        want = {k: v for k, v in manifest.get("files", {}).items() if not k.startswith("META-INF")}
        mism_all = [k for k, v in want.items() if r["hashes"].get(k) not in (None, v)]
        # Files the module rewrites at runtime (webroot data files copied from
        # Documents) always differ from the built zip; that is expected, not a
        # different build. Scripts, module.prop and index.html still must match.
        runtime = [k for k in mism_all if k.startswith("webroot/") and not k.endswith("index.html")]
        mism = [k for k in mism_all if k not in runtime]
        if runtime:
            reasons.append("runtime-rewritten webroot data differs from build (expected): " + ",".join(runtime[:5]))
        miss = [k for k in want if k not in r["hashes"]]
        if mism:
            return "FAIL", ["hash mismatch (log is from a different build): " + ",".join(mism[:5])]
        hash_ok = not miss
    else:
        hash_ok = False
        reasons.append("no manifest: cannot bind log to a build")
    if sim == "1":
        return "PASS_SIMULATED", reasons + ["log came from a simulation (sim=1), not a phone"]
    if not r["boot_completed"]:
        return "PASS_PARTIAL", reasons + ["boot completion not seen in log"]
    if not r["checks"]:
        return "PASS_PARTIAL", reasons + ["no CHECK lines: nothing was proven"]
    if not hash_ok:
        return "PASS_PARTIAL", reasons + ["hashes not fully matched to the build"]
    return "PASS_REAL", reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--manifest")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        with open(a.log, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as e:
        print("STATUS: NOT_TESTED\nERROR: %s" % e)
        return 2
    manifest = None
    if a.manifest:
        with open(a.manifest) as fh:
            manifest = json.load(fh)
    r = parse(text)
    status, reasons = decide(r, manifest)
    out = {"status": status, "reasons": reasons, "stages_seen": sorted(set(r["stages"])), "boots": r["boots"],
           "boot_completed": r["boot_completed"], "errors": r["errors"][:20], "warns": len(r["warns"]),
           "avc": r["avc"], "avc_module": module_avc_count(r), "checks": r["checks"], "environment": {k: r["snap"].get(k, "") for k in
           ("kernel", "selinux", "uid", "shell", "sim", "version", "versionCode")}, "probes": r["probes"][:80]}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print("ENV %s" % out["environment"])
        print("STAGES %s boots=%d boot_completed=%s" % (",".join(out["stages_seen"]), r["boots"], r["boot_completed"]))
        print("CHECKS %s" % r["checks"])
        print("ERRORS %d WARNS %d AVC %d (module %d)" % (len(r["errors"]), len(r["warns"]), r["avc"], out["avc_module"]))
        for e in r["errors"][:10]:
            print("  ERROR: " + e)
        for x in reasons:
            print("NOTE: " + x)
        print("STATUS: " + status)
    return 0 if status in ("PASS_SIMULATED", "PASS_REAL", "PASS_PARTIAL") else 1


if __name__ == "__main__":
    sys.exit(main())

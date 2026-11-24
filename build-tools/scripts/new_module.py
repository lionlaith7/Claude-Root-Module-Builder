#!/usr/bin/env python3
"""new_module.py - create a Magisk/KernelSU module folder from the templates.

Usage:
  python3 -I new_module.py --list
  python3 -I new_module.py --kind basic --id my_mod --name "My Mod" --desc "What it does" --out ./work

Kinds: basic, service, props, canary. Never overwrites an existing folder.
Kid note: this makes a new module folder from a ready pattern, with the diary (log) already built in.
"""
import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(os.path.dirname(HERE), "assets", "templates")
ID_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9._-]+$")
KINDS = {
    "basic": "one-time work at boot, checked and logged",
    "service": "background service: one copy only, config file, loop",
    "props": "system properties (system.prop) plus a check that they applied",
    "canary": "read-only probe: documents what this device supports",
}
TEXT_EXT = (".sh", ".prop", ".md", ".list", "")


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(2)


def copy_tree(src, dst):
    for root, _dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        out = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(out, exist_ok=True)
        for f in files:
            shutil.copyfile(os.path.join(root, f), os.path.join(out, f))


def substitute(folder, tokens):
    for root, _d, files in os.walk(folder):
        for f in files:
            p = os.path.join(root, f)
            if f == "update-binary":
                continue  # official installer: never touched
            with open(p, "rb") as fh:
                data = fh.read()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            for k, v in tokens.items():
                text = text.replace(k, v)
            text = text.replace("\r\n", "\n")
            with open(p, "wb") as fh:
                fh.write(text.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--kind", choices=sorted(KINDS))
    ap.add_argument("--id")
    ap.add_argument("--name")
    ap.add_argument("--desc", default="")
    ap.add_argument("--version", default="v1.0.0")
    ap.add_argument("--versioncode", type=int, default=1)
    ap.add_argument("--author", default="you")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    if a.list:
        for k, v in KINDS.items():
            print("%-8s %s" % (k, v))
        return 0
    if not (a.kind and a.id and a.name):
        fail("--kind, --id and --name are required (or use --list)")
    if not ID_RE.match(a.id):
        fail("id must match ^[a-zA-Z][a-zA-Z0-9._-]+$ (at least 2 chars)")
    dest = os.path.join(a.out, a.id)
    if os.path.exists(dest):
        fail("%s already exists; refusing to overwrite" % dest)
    os.makedirs(dest)
    copy_tree(os.path.join(TPL, "_common"), dest)
    copy_tree(os.path.join(TPL, a.kind), dest)
    desc = a.desc or a.name
    tokens = {
        "@ID@": a.id,
        "@IDSAFE@": re.sub(r"[^a-zA-Z0-9_]", "_", a.id),
        "@NAME@": a.name,
        "@VERSION@": a.version,
        "@VERSIONCODE@": str(a.versioncode),
        "@AUTHOR@": a.author,
        "@DESC@": desc.replace("\n", " "),
    }
    substitute(dest, tokens)
    print("CREATED %s (kind=%s)" % (dest, a.kind))
    print("NEXT: edit the YOUR WORK block, then run lint_module.py and build_zip.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())

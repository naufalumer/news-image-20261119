#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261119 entry.

The artwork is pre-rendered: entry.png sits next to this file and is a
1024x1024 image produced by render_front.py (AI-generated panel
illustrations composited with exact vector text by PIL). This script
uses only the Python standard library. It copies entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output), refusing to write an
oversized file, and verifies the delivered copy is byte-identical to
the source before exiting.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print(f"missing {src}", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the {MAX_BYTES} limit",
              file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if not (magic.startswith(b"\x89PNG") or magic.startswith(b"\xff\xd8\xff")):
        print("entry.png is neither a PNG nor a JPEG file",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    if _sha256(dst) != _sha256(src):
        print("copy failed integrity check", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261122 bounty (v2).

The repository holds one finished front page, entry.png, drawn by the
companion program frontpage.py. This program delivers those exact
bytes to the grader's output path:

    /output/entry.png     (or $MAKEFUN_OUTPUT_DIR/entry.png locally)

Before copying, it checks the payload against the bounty's own gate
limits -- PNG signature, at most 1024 x 1024 pixels, at most 1 MiB --
and after copying it verifies the written file by SHA-256 digest, so
a corrupt or truncated delivery fails loudly instead of scoring 0.
Standard library only, no network, and every run writes the same
bytes.
"""

import hashlib
import os
import struct
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def png_dimensions(blob: bytes) -> tuple[int, int]:
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG (bad signature)")
    # IHDR is the first chunk: width and height are big-endian uint32
    # at fixed offsets 16 and 20.
    return struct.unpack(">II", blob[16:24])


def main() -> None:
    here = Path(__file__).resolve().parent
    payload = (here / "entry.png").read_bytes()

    width, height = png_dimensions(payload)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"image too large: {width}x{height}")
    if len(payload) > MAX_BYTES:
        raise SystemExit(f"image too heavy: {len(payload)} bytes")
    digest = hashlib.sha256(payload).hexdigest()

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(payload)

    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise SystemExit(f"copy failed verification: {target}")
    print(f"delivered {target} ({len(payload)} bytes, {width}x{height}, "
          f"sha256 {digest[:16]}...)")


if __name__ == "__main__":
    main()

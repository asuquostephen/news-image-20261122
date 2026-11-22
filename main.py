#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261122 bounty.

The repository holds one finished picture, entry.png, drawn by the
companion program draw.py. This program places those exact bytes where
the grader reads them:

    /output/entry.png        (or $MAKEFUN_OUTPUT_DIR/entry.png locally)

Standard library only, no network. The copy is checked by SHA-256
digest before the program reports success, and every run writes the
same bytes, as the bounty rules require.
"""

import hashlib
import os
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    payload = (here / "entry.png").read_bytes()
    digest = hashlib.sha256(payload).hexdigest()

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(payload)

    check = hashlib.sha256(target.read_bytes()).hexdigest()
    if check != digest:
        raise SystemExit(f"copy failed verification: {target}")
    print(f"delivered {target} ({len(payload)} bytes, sha256 {digest[:16]}…)")


if __name__ == "__main__":
    main()

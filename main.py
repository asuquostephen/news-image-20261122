#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261122 bounty.

The repository carries one finished picture, ``entry.png``, drawn by the
companion program ``draw.py``. This program's whole job is to place those
exact bytes at the output location the grader reads:

    /output/entry.png            (or $MAKEFUN_OUTPUT_DIR/entry.png locally)

It uses only the Python standard library, touches no network, and writes
the identical bytes on every run, as the bounty rules require.
"""

import os
import shutil
from pathlib import Path


def deliver() -> Path:
    """Copy the bundled picture to the output directory; return its path.

    The copy is verified against the source before returning: the bytes
    are compared in full, and a short or mismatched write raises instead
    of handing the grader a bad file.
    """
    here = Path(__file__).resolve().parent
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    source = here / "entry.png"
    shutil.copyfile(source, target)
    if target.read_bytes() != source.read_bytes():
        raise IOError(f"copy mismatch: {target} vs {source}")
    return target


if __name__ == "__main__":
    written = deliver()
    print(f"delivered {written} ({written.stat().st_size} bytes)")

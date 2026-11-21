"""AERLUME - The Poster for a Place That Isn't There.

Writes one vintage travel-poster image to /output/entry.png: a lighthouse
on a floating island above a sea of clouds at sunset, an airship passing by.

Stdlib only: the poster is a pre-rendered asset (poster.png, drawn at build
time with Pillow - see draw_poster.py); this program just copies it to the
output directory, so it runs in the sandbox with no network and no installs.
"""

import os
import shutil
from pathlib import Path


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "poster.png"
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

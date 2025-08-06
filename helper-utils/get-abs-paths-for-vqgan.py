#!/usr/bin/env python3
"""
Build lists of absolute image paths for dataset splits.

It scans the following operations under a dataset root:
  - remove, translate, rotate

For each operation it looks for split folders:
  - train, test, val

All occurrences of files named exactly "1.png" or "2.png" anywhere under each
split (recursively) are listed. One output file per op/split is created:
  <outdir>/<op>_<split>.txt

Usage:
  python build_image_lists.py --root /path/to/DATASET --outdir /path/to/lists
  # If --outdir is omitted, files are written next to each op folder.
"""

from pathlib import Path
import argparse
from typing import Iterable, List

OPS = ("remove", "translate", "rotate")
SPLITS = ("train", "test", "val")
TARGET_NAMES = {"1.png", "2.png"}


def find_target_images(split_dir: Path) -> List[Path]:
    """Return sorted absolute Paths to 1.png and 2.png under split_dir."""
    if not split_dir.exists():
        return []
    paths = [
        p.resolve()
        for p in split_dir.rglob("*")
        if p.is_file() and p.name in TARGET_NAMES
    ]
    # Deterministic ordering: by parent dir then filename
    paths.sort(key=lambda p: (str(p.parent), p.name))
    return paths


def write_list(paths: Iterable[Path], outfile: Path) -> int:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w", encoding="utf-8") as f:
        for p in paths:
            f.write(str(p) + "\n")
    return len(list(paths))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path,
                        help="Path to DATASET root that contains remove/translate/rotate")
    parser.add_argument("--outdir", type=Path, default=None,
                        help="Directory to write list files. Defaults to each op folder.")
    args = parser.parse_args()

    root: Path = args.root
    outdir: Path | None = args.outdir

    for op in OPS:
        op_dir = root / op
        if not op_dir.exists():
            print(f"[skip] {op_dir} (not found)")
            continue

        for split in SPLITS:
            split_dir = op_dir / split
            paths = find_target_images(split_dir)
            # Choose where to write
            target_outdir = outdir if outdir is not None else op_dir
            outfile = target_outdir / f"{op}_{split}.txt"
            count = write_list(paths, outfile)
            print(f"[ok] {outfile}  ({count} paths)")

if __name__ == "__main__":
    main()

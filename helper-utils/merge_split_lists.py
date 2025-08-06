#!/usr/bin/env python3
from pathlib import Path
import argparse
import glob

SPLITS = ("train", "val", "test")

def read_lines(fp: Path):
    with open(fp, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                return s

def iter_lines(fp: Path):
    with open(fp, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                yield s

def merge_split(src_dir: Path, split: str, out_dir: Path):
    files = sorted(set(glob.glob(str(src_dir / f"*_{split}.txt"))))
    if not files:
        print(f"[warn] no *_{split}.txt files in {src_dir}")
        return
    seen, merged = set(), []
    for f in files:
        for line in iter_lines(Path(f)):
            if line not in seen:
                seen.add(line)
                merged.append(line)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{split}.txt"
    with open(out_path, "w", encoding="utf-8") as out:
        for l in merged:
            out.write(l + "\n")
    print(f"[ok] {split}: merged {len(files)} files -> {out_path} ({len(merged)} lines)")

def main():
    ap = argparse.ArgumentParser(description="Merge *_train/val/test.txt into train/val/test.txt")
    ap.add_argument("--dir", required=True, type=Path,
                    help="Folder containing files like remove_train.txt, rotate_val.txt, etc.")
    ap.add_argument("--outdir", type=Path, default=None,
                    help="Where to write merged files (default: same as --dir)")
    args = ap.parse_args()

    src = args.dir
    outdir = args.outdir or src
    for split in SPLITS:
        merge_split(src, split, outdir)

if __name__ == "__main__":
    main()

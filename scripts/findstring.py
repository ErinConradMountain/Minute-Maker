import argparse
import sys
from pathlib import Path


def find_string(root: Path, needle: str) -> int:
    found = False
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if needle in text:
            print(p.as_posix())
            found = True
    return 0 if found else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Find files containing a string")
    parser.add_argument("needle", help="String to search for")
    parser.add_argument("path", nargs="?", default=".", help="Root path to search")
    args = parser.parse_args(argv)
    return find_string(Path(args.path), args.needle)


if __name__ == "__main__":
    raise SystemExit(main())


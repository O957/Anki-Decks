"""
This script is used as a pre-commit hook to get the files
names of media files from a target media directory. These
media files are used across the Anki decks.
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = (SCRIPT_DIR / ".." / ".." / "Anki-Decks-Media").resolve()
OUTPUT_FILE = (SCRIPT_DIR / ".." / "assets" / "media_files.json").resolve()

if not MEDIA_DIR.is_dir():
    print(f"Error: media directory not found at {MEDIA_DIR}", file=sys.stderr)
    sys.exit(1)

files = []
for path in MEDIA_DIR.rglob("*"):
    if path.is_file():
        files.append(path.name)
files = sorted(files)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(files, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(files)} media filenames to {OUTPUT_FILE}")

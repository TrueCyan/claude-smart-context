#!/usr/bin/env python3
"""
Load Archive
Searches and loads a previous context archive.

Usage: python3 load_archive.py "search term"
"""
import sys
from pathlib import Path

# Force UTF-8 encoding for stdin/stdout (Windows compatibility)
sys.stdin.reconfigure(encoding='utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARCHIVE_DIR = Path.home() / ".claude" / "context_history" / "archives"

query = " ".join(sys.argv[1:]).lower() if len(sys.argv) > 1 else ""

if not query:
    print("Usage: python3 load_archive.py \"search term\"")
    sys.exit(1)

if not ARCHIVE_DIR.exists():
    print("No archives found")
    sys.exit(0)

# Search archives
found = False
for f in sorted(ARCHIVE_DIR.glob("*.md"), reverse=True):
    try:
        content = f.read_text(encoding='utf-8')
        if query in content.lower() or query in f.name.lower():
            print(f"# Loaded Archive: {f.name}\n")
            print(content)
            found = True
            break
    except Exception as e:
        continue

if not found:
    # List available archives
    archives = sorted(ARCHIVE_DIR.glob("*.md"), reverse=True)[:5]
    if archives:
        print(f"No archive matching '{query}' found.\n")
        print("Available archives:")
        for a in archives:
            print(f"  - {a.name}")
    else:
        print("No archives available")

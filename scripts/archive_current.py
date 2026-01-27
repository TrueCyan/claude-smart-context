#!/usr/bin/env python3
"""
Archive Current Context
Archives the current context and prepares for /clear.

Usage: python3 archive_current.py "Title" "keyword1,keyword2"
"""
import sys
from pathlib import Path
from datetime import datetime

CONTEXT_DIR = Path.home() / ".claude" / "context_history"
CURRENT = CONTEXT_DIR / "current_context.md"
ARCHIVE_DIR = CONTEXT_DIR / "archives"
CLEAR_FLAG = CONTEXT_DIR / ".clear_flag"

# Ensure directories exist
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Parse arguments
title = sys.argv[1] if len(sys.argv) > 1 else "untitled"
keywords = sys.argv[2] if len(sys.argv) > 2 else ""

# Archive current context
if CURRENT.exists():
    content = CURRENT.read_text(encoding='utf-8').strip()
    if content:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize title for filename
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:30].strip().replace(" ", "_")
        archive_file = ARCHIVE_DIR / f"{timestamp}_{safe_title}.md"

        archive_content = f"""# {title}

## Keywords
{keywords}

## Archived At
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{content}
"""
        archive_file.write_text(archive_content, encoding='utf-8')
        print(f"Archived: {archive_file.name}")
    else:
        print("No content to archive")
else:
    print("No current context file")

# Clear current context and set flag
CURRENT.write_text("", encoding='utf-8')
CLEAR_FLAG.write_text("1", encoding='utf-8')
print("Ready for /clear")

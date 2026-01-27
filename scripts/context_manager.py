#!/usr/bin/env python3
"""
Smart Context Manager - prompt_submit hook
Handles context injection, comparison, and switching detection.
"""
import os
import re
from pathlib import Path
from datetime import datetime

# Context storage directory
CONTEXT_DIR = Path.home() / ".claude" / "context_history"
CURRENT = CONTEXT_DIR / "current_context.md"
ARCHIVE_DIR = CONTEXT_DIR / "archives"
CLEAR_FLAG = CONTEXT_DIR / ".clear_flag"

# Ensure directories exist
CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def get_archives(limit: int = 10) -> list:
    """Get list of archived contexts (newest first)"""
    archives = []
    for f in sorted(ARCHIVE_DIR.glob("*.md"), reverse=True)[:limit]:
        try:
            content = f.read_text(encoding='utf-8')
            # Extract title
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f.stem
            # Extract keywords
            keywords_match = re.search(r'## Keywords\n(.+)', content)
            keywords = keywords_match.group(1).strip() if keywords_match else ""
            archives.append({
                "file": f.name,
                "title": title,
                "keywords": keywords,
            })
        except Exception:
            continue
    return archives


def main():
    # Case 1: Just after /clear - restore context
    if CLEAR_FLAG.exists():
        CLEAR_FLAG.unlink()
        if CURRENT.exists():
            summary = CURRENT.read_text(encoding='utf-8').strip()
            if summary:
                print(f"""<context-restored>
{summary}

---
Above context has been restored. Continue your work with this context.
</context-restored>""")
        return

    # Load current context
    current = ""
    if CURRENT.exists():
        current = CURRENT.read_text(encoding='utf-8').strip()

    # Get archive list
    archives = get_archives(5)
    archive_list = "\n".join([f"- **{a['title']}** ({a['file']})" for a in archives])

    if current:
        print(f"""<context-check>
## Current Context
{current}

## Previous Archives
{archive_list if archive_list else "(none)"}

---
Analyze the user's request:

1. **Previous context question** (e.g., "what did we do before", "that API work"):
   → Run: `python3 ~/.claude/scripts/load_archive.py "search term"`

2. **Continue current context**:
   → Proceed normally

3. **New/different task**:
   → First update current_context.md with final summary
   → Run: `python3 ~/.claude/scripts/archive_current.py "Title" "keyword1,keyword2"`
   → Execute: `/clear`
</context-check>""")
    else:
        # No current context - always show message
        print(f"""<context-info>
No active context. Starting fresh.

## Previous Archives
{archive_list if archive_list else "(none)"}

Save your work progress with:
```bash
cat > ~/.claude/context_history/current_context.md << 'EOF'
## Current Task
[Task title]

## Summary
[Progress]

## Files Modified
- [files]
EOF
```
</context-info>""")


if __name__ == "__main__":
    main()

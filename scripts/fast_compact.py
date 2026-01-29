#!/usr/bin/env python3
"""
Fast Compact - PreCompact hook
Intercepts auto-compact and replaces with faster /clear approach.
Includes gap log (tool calls since last summary) in the archive.
"""
import sys
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding for stdin/stdout (Windows compatibility)
sys.stdin.reconfigure(encoding='utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CONTEXT_DIR = Path.home() / ".claude" / "context_history"
CURRENT = CONTEXT_DIR / "current_context.md"
ARCHIVE_DIR = CONTEXT_DIR / "archives"
CLEAR_FLAG = CONTEXT_DIR / ".clear_flag"
GAP_LOG = CONTEXT_DIR / ".gap_log"

# Ensure directories exist
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Read gap log if exists
gap_content = ""
if GAP_LOG.exists():
    gap_content = GAP_LOG.read_text(encoding='utf-8').strip()

# Archive current context if exists
if CURRENT.exists():
    content = CURRENT.read_text(encoding='utf-8').strip()
    if content or gap_content:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = ARCHIVE_DIR / f"{timestamp}_auto_compact.md"

        # Build archive with gap log appended
        sections = [f"""# Auto-archived (Context Full)

## Keywords
auto-compact, context-overflow

## Archived At
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""]

        if content:
            sections.append(content)

        if gap_content:
            sections.append(f"""## Recent Activity (since last summary)
```
{gap_content}
```""")

        archive_file.write_text("\n\n".join(sections), encoding='utf-8')

# Clear gap log
if GAP_LOG.exists():
    GAP_LOG.write_text("", encoding='utf-8')

# Set clear flag
CLEAR_FLAG.write_text("1", encoding='utf-8')

# Instruct Claude to use /clear instead
print("""<system-reminder>
[Context Full - Fast Compact]
Execute `/clear` now. Your context will be automatically restored.
This is faster than standard compact.
</system-reminder>""")

# Exit code 2 blocks the default compact
sys.exit(2)

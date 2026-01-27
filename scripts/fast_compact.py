#!/usr/bin/env python3
"""
Fast Compact - PreCompact hook
Intercepts auto-compact and replaces with faster /clear approach.
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

# Archive current context if exists
if CURRENT.exists():
    content = CURRENT.read_text(encoding='utf-8').strip()
    if content:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = ARCHIVE_DIR / f"{timestamp}_auto_compact.md"

        archive_content = f"""# Auto-archived (Context Full)

## Keywords
auto-compact, context-overflow

## Archived At
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{content}
"""
        archive_file.write_text(archive_content, encoding='utf-8')

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

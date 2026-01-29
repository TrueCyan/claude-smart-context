#!/usr/bin/env python3
"""
Smart Context Manager - UserPromptSubmit hook
Handles session detection, context injection, and agent invocation instructions.
"""
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding for stdin/stdout (Windows compatibility)
sys.stdin.reconfigure(encoding='utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Context storage directory
CONTEXT_DIR = Path.home() / ".claude" / "context_history"
CURRENT = CONTEXT_DIR / "current_context.md"
ARCHIVE_DIR = CONTEXT_DIR / "archives"
CLEAR_FLAG = CONTEXT_DIR / ".clear_flag"
LAST_SESSION_FILE = CONTEXT_DIR / ".last_session_id"

# Ensure directories exist
CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Agent invocation instruction injected into every prompt
AGENT_INSTRUCTION = """<context-rules>
After completing meaningful work (task completion, file modifications, key decisions),
call the context-manager agent to update the context summary.
</context-rules>"""


def read_session_id() -> str:
    """Read session_id from stdin (passed by hook system)."""
    try:
        data = json.loads(sys.stdin.read())
        return data.get("session_id", "")
    except Exception:
        return ""


def get_last_session_id() -> str:
    """Read the last known session ID."""
    if LAST_SESSION_FILE.exists():
        return LAST_SESSION_FILE.read_text(encoding='utf-8').strip()
    return ""


def save_session_id(session_id: str):
    """Save the current session ID."""
    if session_id:
        LAST_SESSION_FILE.write_text(session_id, encoding='utf-8')


def archive_current_context():
    """Move current_context.md to archives."""
    if not CURRENT.exists():
        return
    content = CURRENT.read_text(encoding='utf-8').strip()
    if not content:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Extract task title from content
    title_match = re.search(r'^## Current Task\s*\n(.+)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "session"
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:30].strip().replace(" ", "_")

    archive_file = ARCHIVE_DIR / f"{timestamp}_{safe_title}.md"
    archive_content = f"""# {title}

## Keywords
auto-session-switch

## Archived At
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{content}
"""
    archive_file.write_text(archive_content, encoding='utf-8')
    # Clear current context for new session
    CURRENT.write_text("", encoding='utf-8')


def get_archives(limit: int = 5) -> list:
    """Get list of archived contexts (newest first)."""
    archives = []
    for f in sorted(ARCHIVE_DIR.glob("*.md"), reverse=True)[:limit]:
        try:
            content = f.read_text(encoding='utf-8')
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f.stem
            archives.append({"file": f.name, "title": title})
        except Exception:
            continue
    return archives


def main():
    # Read session ID from stdin
    session_id = read_session_id()

    # Case 1: Post /clear - restore context
    if CLEAR_FLAG.exists():
        CLEAR_FLAG.unlink()
        if CURRENT.exists():
            summary = CURRENT.read_text(encoding='utf-8').strip()
            if summary:
                print(f"""<context-restored>
{summary}

---
Above context has been restored. Continue your work with this context.
</context-restored>

{AGENT_INSTRUCTION}""")
                return

    # Detect session change
    last_session_id = get_last_session_id()
    session_changed = bool(session_id and last_session_id and session_id != last_session_id)

    if session_changed:
        # Archive previous session's context
        archive_current_context()

    # Save current session ID
    save_session_id(session_id)

    # Load current context
    current = ""
    if CURRENT.exists():
        current = CURRENT.read_text(encoding='utf-8').strip()

    # Get archive list
    archives = get_archives(5)
    archive_list = "\n".join([f"- **{a['title']}** ({a['file']})" for a in archives])

    if session_changed:
        # New session - previous context was archived
        print(f"""<context-info>
New session detected. Previous context has been archived.

## Previous Archives
{archive_list if archive_list else "(none)"}

To access previous work, use the context-manager agent to search archives.
</context-info>

{AGENT_INSTRUCTION}""")
    elif current:
        print(f"""<context-check>
## Current Context
{current}

## Previous Archives
{archive_list if archive_list else "(none)"}
</context-check>

{AGENT_INSTRUCTION}""")
    else:
        # No current context, fresh start
        print(f"""<context-info>
No active context. Starting fresh.

## Previous Archives
{archive_list if archive_list else "(none)"}
</context-info>

{AGENT_INSTRUCTION}""")


if __name__ == "__main__":
    main()

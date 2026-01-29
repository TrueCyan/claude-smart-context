#!/usr/bin/env python3
"""
Tool Logger - PostToolUse hook
Logs tool calls to a gap log file for PreCompact to use.
Rule-based: no AI, just tool name + file path.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

sys.stdin.reconfigure(encoding='utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CONTEXT_DIR = Path.home() / ".claude" / "context_history"
GAP_LOG = CONTEXT_DIR / ".gap_log"

CONTEXT_DIR.mkdir(parents=True, exist_ok=True)

# File path keys commonly found in tool_input
FILE_PATH_KEYS = ["file_path", "path", "pathInProject", "filePath", "command"]


def extract_file_path(tool_input: dict) -> str:
    """Extract the most relevant file path from tool input."""
    for key in FILE_PATH_KEYS:
        val = tool_input.get(key, "")
        if val and isinstance(val, str):
            # For command (Bash), just take first 80 chars
            if key == "command":
                return val[:80]
            return val
    return ""


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if not tool_name:
        return

    # Skip logging the context-manager agent itself to avoid noise
    if tool_name == "Task" and "context-manager" in str(tool_input.get("prompt", "")):
        return

    file_path = extract_file_path(tool_input)
    timestamp = datetime.now().strftime("%H:%M:%S")

    line = f"[{timestamp}] {tool_name}"
    if file_path:
        line += f": {file_path}"

    # Append to gap log
    with open(GAP_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()

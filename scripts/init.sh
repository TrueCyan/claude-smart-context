#!/bin/bash
# Smart Context Plugin Initialization (Unix)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INIT_FLAG="$PLUGIN_ROOT/.initialized"
VENV_PATH="$PLUGIN_ROOT/.venv"
CONTEXT_DIR="$HOME/.claude/context_history"

# Already initialized → exit immediately
[ -f "$INIT_FLAG" ] && exit 0

echo "[smart-context] Initializing plugin..."

# Check Python availability
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[smart-context] ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

# Create virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "[smart-context] Creating Python virtual environment..."
    $PYTHON_CMD -m venv "$VENV_PATH"
fi

# Create context directories
mkdir -p "$CONTEXT_DIR/archives"

# Mark as initialized
touch "$INIT_FLAG"
echo "[smart-context] Plugin initialized successfully"

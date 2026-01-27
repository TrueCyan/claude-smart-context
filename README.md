# claude-smart-context

Smart context management plugin for Claude Code.

## Features

- **Fast Compaction**: Uses `/clear` instead of slow LLM-based `/compact`
- **Progressive Summarization**: Continuously saves context to external files
- **Auto Context Switching**: Detects task changes and manages transitions
- **Archive Access**: Instantly load previous work context

## How It Works

```
[Normal Work]
     │
     ▼
[Task Complete] → Update current_context.md (progressive)
     │
     ▼
[Context Full OR Task Switch]
     │
     ▼
[Archive] → Save to archives/
     │
     ▼
[/clear] → Fast reset (no LLM summarization)
     │
     ▼
[Next Prompt] → Auto-restore context from file
```

## Installation

### Option 1: Direct Install

```bash
/plugin install TrueCyan/claude-smart-context
```

### Option 2: Via Marketplace

```bash
/plugin marketplace add TrueCyan/claude-smart-context
/plugin install claude-smart-context
```

## Usage

Once installed, the plugin works automatically:

1. **Automatic Context Injection**: Every prompt receives current context info
2. **Progressive Saving**: Update context after meaningful work
3. **Fast Compact**: When context is full, uses `/clear` instead of `/compact`
4. **Archive Access**: Ask about previous work to load from archives

### Commands (via Claude)

```bash
# Archive current context and switch
python3 ~/.claude/scripts/archive_current.py "Task Title" "keyword1,keyword2"
/clear

# Load previous context
python3 ~/.claude/scripts/load_archive.py "search term"
```

## File Structure

```
~/.claude/context_history/
├── current_context.md      # Active context (progressive updates)
├── .clear_flag             # Signal for context restoration
└── archives/               # Previous contexts
    ├── 20250127_143052_API_work.md
    └── ...
```

## Context File Format

```markdown
## Current Task
JWT Authentication Implementation

## Summary
Completed login/logout API. Working on token refresh.

## Files Modified
- src/auth/login.ts
- src/auth/logout.ts

## Key Decisions
- Access token: 1 hour expiry
- Refresh token: 7 days expiry

## Next Steps
- Implement token refresh endpoint
- Add tests
```

## Why This Plugin?

| Standard Compact | Smart Context |
|-----------------|---------------|
| Slow (LLM call) | Fast (/clear) |
| Context loss risk | Explicit saves |
| No history | Archive access |
| Manual only | Auto-detection |

## Requirements

- Claude Code CLI
- Python 3.7+

## License

MIT

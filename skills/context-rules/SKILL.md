---
name: context-rules
description: Context management rules. Apply when managing conversation context, completing tasks, or switching between different work.
---

# Smart Context Management Rules

## Progressive Summarization (After Task Completion)

After completing meaningful work (file modifications, feature implementation, bug fixes), update the context file:

```bash
cat > ~/.claude/context_history/current_context.md << 'EOF'
## Current Task
[Task title - what you're working on]

## Summary
[Current progress and status]

## Files Modified
- [List of modified files]

## Key Decisions
- [Important decisions made]

## Next Steps
- [What to do next]
EOF
```

## Context Switching

When `<context-check>` message is received, analyze the user's request:

1. **Same context** → Continue working normally
2. **Question about previous work** → Run `python3 ~/.claude/scripts/load_archive.py "search term"`
3. **New/different task**:
   - Update current_context.md with final summary
   - Run `python3 ~/.claude/scripts/archive_current.py "Title" "keywords"`
   - Execute `/clear`

## After /clear

When `<context-restored>` message is received, use the provided context to continue work seamlessly.

## When to Update Context

- After modifying 3+ files
- After completing a feature or fix
- After making important decisions
- Before switching to a different task

---
name: context-rules
description: Context management rules. Apply when managing conversation context, completing tasks, or switching between different work.
---

# Smart Context Management Rules

## Automatic Context Saving (Agent-Based)

After completing meaningful work (file modifications, feature implementation, bug fixes, key decisions), call the **context-manager** agent to automatically summarize and save context.

The agent will:
- Analyze the current conversation
- Create/update `~/.claude/context_history/current_context.md` with a structured summary
- Handle archiving when switching tasks

You do NOT need to manually write context files. The agent handles everything.

## When to Call context-manager Agent

- After completing a task or subtask
- After modifying 3+ files
- After making important architectural decisions
- Before switching to a different task
- When the user explicitly asks to save context

## Context Switch Detection

When `<context-rules>` includes a `Current task:` line, compare it to the user's new request:

**Same context** (proceed normally):
- Same project, same feature, same bug
- Follow-up questions about current work
- "commit this", "test this", "push" etc.

**Different context** (switch required):
- Completely different project or codebase
- Unrelated feature or topic
- Different technology domain (e.g., was doing Unity C#, now asking about Python plugin)

**When switching context:**
1. Call context-manager agent to archive current context
2. Execute `/clear` to free up the context window
3. Begin the new task fresh

## Context Switching (Manual)

When `<context-check>` message is received without automatic detection:

1. **Same context** - Continue working normally
2. **Question about previous work** - Call context-manager agent to search archives
3. **New/different task** - Call context-manager agent to archive current context, then `/clear`

## After /clear

When `<context-restored>` message is received, use the provided context to continue work seamlessly.

## Session Changes

When `<context-info>` indicates a new session was detected:
- Previous context has been automatically archived
- Start fresh or ask context-manager agent to load relevant archives

## Archive Access

To find previous work, call the context-manager agent. It can:
- Search archive files by content
- Load and display archived context
- Help restore previous working state

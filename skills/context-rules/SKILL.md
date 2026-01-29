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

When `<context-rules>` includes `Current task:` and `Previous tasks:`, compare the user's request:

### 1. Same as current task → Proceed normally
- Same project, same feature, same bug
- Follow-up questions about current work
- "commit this", "test this", "push" etc.

### 2. Matches a previous task → Restore from archive
- User mentions work from a previous task listed in `Previous tasks:`
- e.g., "이전에 했던 API 작업 이어서 해줘", "그 Unity 빌드 설정 다시 보자"
- **Action:**
  1. Call context-manager agent to archive current context
  2. Call context-manager agent to load the matching archive
  3. Execute `/clear` to restore with the loaded context

### 3. Completely new task → Archive and start fresh
- Unrelated project, feature, or technology domain
- Nothing matching in current or previous tasks
- **Action:**
  1. Call context-manager agent to archive current context
  2. Execute `/clear`
  3. Begin the new task fresh

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

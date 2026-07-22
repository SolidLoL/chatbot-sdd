---
name: speckit-tasks
description: Generate actionable task lists for implementation. Use when asked to create tasks, break down work, or generate implementation tasks.
---

# speckit-tasks

Breaks down a technical plan into actionable tasks in `specs/tasks/`.

## Usage

```bash
bash .opencode/skills/speckit-tasks/speckit-tasks.sh
```

## Workflow

1. Read the plan from `specs/plans/<feature>.md`
2. Decompose into tasks with:
   - Unique ID (T-001, T-002, ...)
   - Descriptive title
   - Files to modify
   - Dependencies (task IDs)
   - Effort estimate (S/M/L)
   - Acceptance criteria
3. Write to `specs/tasks/<feature>.md`
4. Each task should be ≤ half-day of work

Call this skill when:
- Asked to "create tasks", "break down work", "generate task list"
- After speckit-plan has defined the technical approach
- Need to estimate and sequence implementation work

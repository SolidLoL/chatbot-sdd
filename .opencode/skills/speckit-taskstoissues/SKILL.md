---
name: speckit-taskstoissues
description: Convert generated task lists into GitHub issues for tracking and execution. Use when asked to create GitHub issues, export tasks, or sync with GitHub.
---

# speckit-taskstoissues

Converts `specs/tasks/<feature>.md` into GitHub Issues.

## Usage

```bash
bash .opencode/skills/speckit-taskstoissues/speckit-taskstoissues.sh
```

## Workflow

1. Read task list from `specs/tasks/<feature>.md`
2. For each task without an Issue URL:
   - Create GitHub Issue with title, body, labels
   - Append URL to the task list
3. Update `specs/tasks/<feature>.md` with links

Requires `gh` CLI authenticated.

Call this skill when:
- Asked to "create issues", "export to GitHub", "sync tasks"
- After speckit-tasks has defined the task list
- Ready to start tracking work in GitHub

---
name: speckit-implement
description: Execute all tasks to build the feature according to the plan. Use when asked to implement, build, or code a feature following the plan.
---

# speckit-implement

Executes tasks from `specs/tasks/<feature>.md` in dependency order.

## Usage

```bash
bash .opencode/skills/speckit-implement/speckit-implement.sh
```

## Workflow

1. Read task list from `specs/tasks/<feature>.md`
2. For each pending task in dependency order:
   - Read spec and plan for context
   - Implement the changes
   - Regenerate types (openapi-typescript, datamodel-codegen)
   - Run tests (pytest, vitest)
   - Mark task complete in task list
3. If a task fails, stop and report

Call this skill when:
- Asked to "implement", "build", "code the feature"
- After speckit-tasks has defined the task list
- Ready to write code following the plan

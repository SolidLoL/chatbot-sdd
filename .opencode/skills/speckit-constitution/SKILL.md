---
name: speckit-constitution
description: Create or update project governing principles and development guidelines. Use when asked to define constitution, principles, governance, or project guidelines.
---

# speckit-constitution

Creates or updates `specs/CONSTITUTION.md` with the project's governing principles.

## Usage

```bash
bash .opencode/skills/speckit-constitution/speckit-constitution.sh
```

## Workflow

1. Check if `specs/CONSTITUTION.md` exists
2. If it exists: read current constitution, ask user what to change, then update
3. If it doesn't exist: interview user on project values, stack, principles, then generate
4. Sections to cover: Mission, Core Values, Architecture Principles, Tech Stack Rationale, Code Standards, Testing Philosophy, Development Workflow, Decision Log
5. Write/overwrite `specs/CONSTITUTION.md` with the result

Call this skill when:
- Asked to "create constitution", "set principles", "define governance"
- Starting a new project phase that needs guiding principles
- Reviewing or updating project development guidelines
- The project needs a decision-making framework

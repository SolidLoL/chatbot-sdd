---
name: speckit-specify
description: Define what you want to build (requirements and user stories). Use when asked to specify requirements, write user stories, or define a feature.
---

# speckit-specify

Creates detailed specifications with user stories and acceptance criteria in `specs/<feature>/`.

## Usage

```bash
bash .opencode/skills/speckit-specify/speckit-specify.sh
```

## Workflow

1. Ask user what feature they want to build
2. Research existing codebase and OpenAPI spec for context
3. Create `specs/<feature-name>/README.md` with:
   - Problem context
   - User stories (role, action, benefit)
   - Acceptance criteria (testable conditions)
   - Edge cases (errors, limits, empty states)
   - Dependencies
4. Review with user before finalizing

Call this skill when:
- Asked to "specify", "write requirements", "define user stories"
- Planning a new feature
- Need to formalize what needs to be built

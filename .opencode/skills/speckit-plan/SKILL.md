---
name: speckit-plan
description: Create technical implementation plans with your chosen tech stack. Use when asked to plan implementation, design architecture, or create a technical plan.
---

# speckit-plan

Translates specifications into technical implementation plans in `specs/plans/`.

## Usage

```bash
bash .opencode/skills/speckit-plan/speckit-plan.sh
```

## Workflow

1. Read the specification from `specs/<feature>/README.md`
2. Analyze current codebase architecture for integration points
3. Create `specs/plans/<feature>.md` with:
   - Architecture: components and connections
   - OpenAPI changes (if any)
   - Backend changes: routes, services, models
   - Frontend changes: components, hooks, types
   - Data flow diagram (ASCII)
   - Risks and mitigations
   - Implementation order
4. Review with user before proceeding

Call this skill when:
- Asked to "plan", "design architecture", "create technical plan"
- After speckit-specify has defined requirements
- Need to figure out how to implement a feature

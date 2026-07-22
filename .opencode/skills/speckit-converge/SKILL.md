---
name: speckit-converge
description: Assess the codebase against spec/plan/tasks and append remaining work. Use when asked to audit, assess progress, check convergence, or verify implementation.
---

# speckit-converge

Audits the current codebase against specs, plans, and task lists. Reports what's done, what's missing, and what's drifted.

## Usage

```bash
bash .opencode/skills/speckit-converge/speckit-converge.sh
```

## Workflow

1. For each feature in `specs/` with a task list:
   - Read spec, plan, and tasks
   - Scan codebase for implementations
   - Compare and classify:
     - ✅ Implemented correctly
     - ⚠️ Implemented but differs from spec
     - ❌ Not implemented
     - 🏚️ Implemented but not specified
   - Update task list with findings
2. Generate convergence report

Call this skill when:
- Asked to "audit", "check progress", "converge", "verify implementation"
- After partial implementation to see what's left
- Before release to validate against specs

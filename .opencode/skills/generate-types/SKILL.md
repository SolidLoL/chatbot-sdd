---
name: generate-types
description: Generate TypeScript types from the OpenAPI spec using openapi-typescript. Use when asked to sync types with the API spec.
---

# generate-types

Generates TypeScript type definitions from `specs/openapi.yaml` to `frontend/src/types/api.ts`.

## Usage

```bash
bash .opencode/skills/generate-types/generate-types.sh
```

Or with a custom spec path:

```bash
bash .opencode/skills/generate-types/generate-types.sh specs/openapi.yaml
```

## What it does

1. Runs `pnpm dlx openapi-typescript` against the OpenAPI spec
2. Outputs typed interfaces to `frontend/src/types/api.ts`
3. Reports success or errors

Call this skill when:
- The OpenAPI spec has changed and frontend types need updating
- Asked to "generate types", "sync types", or "update API types"
- Working on type-safe API integration in the frontend

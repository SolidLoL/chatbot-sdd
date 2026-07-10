---
name: generate-mocks
description: Generate API mocks from the OpenAPI spec using openapi-mockgen. Use when asked to create mock data for frontend testing.
---

# generate-mocks

Generates mock data from `specs/openapi.yaml` to `frontend/mocks/`.

## Usage

```bash
bash .opencode/skills/generate-mocks/generate-mocks.sh
```

Call this skill when:
- Frontend needs mock data for development or testing
- The OpenAPI spec has changed and mocks need regeneration
- Asked to "generate mocks", "create mock data", or "setup API mocks"

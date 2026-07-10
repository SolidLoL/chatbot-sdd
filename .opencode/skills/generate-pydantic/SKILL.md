---
name: generate-pydantic
description: Generate Pydantic models from the OpenAPI spec using datamodel-code-generator. Use when asked to generate backend models from the API spec.
---

# generate-pydantic

Generates Pydantic v2 models from `specs/openapi.yaml` to `backend/models/generated.py`.

## Usage

```bash
bash .opencode/skills/generate-pydantic/generate-pydantic.sh
```

## What it does

1. Runs `datamodel-code-generator` against the OpenAPI spec
2. Outputs Pydantic v2 models to `backend/models/generated.py`
3. Creates `backend/models/__init__.py` re-exporting all models

Call this skill when:
- The OpenAPI spec has changed and backend models need updating
- Asked to "generate pydantic", "generate models", or "sync backend models"
- Working on backend API integration after spec changes

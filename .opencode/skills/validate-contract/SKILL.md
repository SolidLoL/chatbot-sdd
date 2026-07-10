---
name: validate-contract
description: Run contract tests to validate backend API compliance with the OpenAPI spec. Use when asked to verify API conformance.
---

# validate-contract

Runs contract tests via pytest to ensure the backend API matches the OpenAPI specification.

## Usage

```bash
bash .opencode/skills/validate-contract/validate-contract.sh
```

Call this skill when:
- The OpenAPI spec has changed and backend needs validation
- Asked to "validate contract", "run contract tests", or "check API conformance"
- Before deploying to ensure API compliance

---
name: start-mock
description: Start a Prism mock server from the OpenAPI spec. Use when asked to start the API mock server for frontend development.
---

# start-mock

Starts a Prism mock server from `specs/openapi.yaml` on `http://localhost:4010`.

## Usage

```bash
bash .opencode/skills/start-mock/start-mock.sh
```

## What it does

1. Verifies the OpenAPI spec exists
2. Checks no mock is already running on port 4010
3. Launches Prism in background and saves PID to `.mock.pid`

Call this skill when:
- Frontend needs a live mock API for development
- Asked to "start mock", "start mock server", or "launch Prism"
- Setting up the development environment

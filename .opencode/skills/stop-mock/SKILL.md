---
name: stop-mock
description: Stop the Prism mock server. Use when asked to stop the API mock server.
---

# stop-mock

Stops the running Prism mock server.

## Usage

```bash
bash .opencode/skills/stop-mock/stop-mock.sh
```

## What it does

1. Reads the PID from `.mock.pid`
2. Kills the process and cleans up the PID file
3. Falls back to `pkill -f "prism mock"` if no PID file found

Call this skill when:
- Done developing with the mock API
- Asked to "stop mock", "stop mock server", or "kill Prism"
- Need to restart the mock server

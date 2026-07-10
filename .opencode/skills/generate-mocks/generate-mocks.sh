#!/bin/bash
# .opencode/skills/generate-mocks.sh
pnpm dlx openapi-mockgen specs/openapi.yaml -o frontend/mocks/
echo "✅ Mocks generados"
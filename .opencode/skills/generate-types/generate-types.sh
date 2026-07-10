#!/bin/bash
# .opencode/skills/generate-types/generate-types.sh
SPEC="${1:-specs/openapi.yaml}"
OUTPUT="${2:-frontend/src/types/api.ts}"
pnpm dlx openapi-typescript "$SPEC" -o "$OUTPUT"
echo "✅ TypeScript types generated: $OUTPUT"

#!/bin/bash
# .opencode/skills/speckit-implement/speckit-implement.sh

set -e

echo "🔧 Inicializando speckit-implement..."
echo "💡 Necesito un task list en specs/tasks/<feature>.md"
echo ""
echo "Task lists disponibles:"
ls specs/tasks/ 2>/dev/null || echo "  (ninguno aún - usa speckit-tasks primero)"

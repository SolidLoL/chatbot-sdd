#!/bin/bash
# .opencode/skills/speckit-tasks/speckit-tasks.sh

set -e

mkdir -p specs/tasks

echo "📝 Inicializando speckit-tasks..."
echo "💡 Necesito un plan en specs/plans/<feature>.md"
echo "📁 Las tareas se guardarán en specs/tasks/<feature>.md"
echo ""
echo "Planes disponibles:"
ls specs/plans/ 2>/dev/null || echo "  (ninguno aún - usa speckit-plan primero)"

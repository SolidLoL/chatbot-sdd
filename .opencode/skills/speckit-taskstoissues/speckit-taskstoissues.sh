#!/bin/bash
# .opencode/skills/speckit-taskstoissues/speckit-taskstoissues.sh

set -e

echo "🐙 Inicializando speckit-taskstoissues..."

if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) no está instalado."
    echo "   Instálalo desde: https://cli.github.com/"
    exit 1
fi

if ! gh auth status 2>/dev/null; then
    echo "❌ Error: gh no está autenticado."
    echo "   Ejecuta: gh auth login"
    exit 1
fi

echo "💡 Necesito un task list en specs/tasks/<feature>.md"
echo ""
echo "Task lists disponibles:"
ls specs/tasks/ 2>/dev/null || echo "  (ninguno aún - usa speckit-tasks primero)"

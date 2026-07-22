#!/bin/bash
# .opencode/skills/speckit-plan/speckit-plan.sh

set -e

mkdir -p specs/plans

echo "🏗️  Inicializando speckit-plan..."
echo "💡 Necesito una especificación en specs/<feature>/README.md"
echo "📁 El plan se guardará en specs/plans/<feature>.md"
echo ""
echo "Features disponibles:"
ls specs/ 2>/dev/null | grep -v plans | grep -v 'CONSTITUTION\|\.template\|\.md' || echo "  (ninguna aún - usa speckit-specify primero)"

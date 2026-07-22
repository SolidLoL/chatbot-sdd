#!/bin/bash
# .opencode/skills/speckit-converge/speckit-converge.sh

set -e

echo "🔍 Inicializando speckit-converge..."
echo ""
echo "Features para auditar:"
for f in specs/tasks/*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f" .md)
    pending=$(grep -c '\[ \]' "$f" 2>/dev/null || echo 0)
    done_count=$(grep -c '\[x\]' "$f" 2>/dev/null || echo 0)
    total=$((pending + done_count))
    if [ "$total" -gt 0 ]; then
        pct=$((done_count * 100 / total))
        echo "  📁 $name: $pct% completo ($done_count/$total tareas)"
    fi
done
echo ""
echo "💡 Invoca al agente speckit-converge para el análisis detallado."

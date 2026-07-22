#!/bin/bash
# .opencode/skills/speckit-constitution/speckit-constitution.sh

set -e

CONSTITUTION_FILE="specs/CONSTITUTION.md"
TEMPLATE_FILE="specs/CONSTITUTION.md.template"

echo "📜 Inicializando speckit-constitution..."

if [ ! -f "$CONSTITUTION_FILE" ]; then
    echo "📄 No se encontró CONSTITUTION.md. Creando desde template..."
    if [ -f "$TEMPLATE_FILE" ]; then
        cp "$TEMPLATE_FILE" "$CONSTITUTION_FILE"
        echo "✅ Template copiado a $CONSTITUTION_FILE"
    else
        echo "# CONSTITUTION" > "$CONSTITUTION_FILE"
        echo "" >> "$CONSTITUTION_FILE"
        echo "Project constitution will be defined here." >> "$CONSTITUTION_FILE"
        echo "⚠️  Template no encontrado, archivo vacío creado"
    fi
    echo ""
    echo "🔧 Revisa $CONSTITUTION_FILE y completa las secciones."
    echo "💡 Luego invoca speckit-constitution nuevamente para refinarlo con el agente."
else
    echo "✅ CONSTITUTION.md exists ($(wc -l < "$CONSTITUTION_FILE") lines)"
    echo "💡 Invoca al agente speckit-constitution para revisarlo o actualizarlo."
fi

#!/bin/bash
# .opencode/skills/start-mock.sh

set -e

echo "🔄 Iniciando mock server desde OpenAPI..."

# Verifica que openapi.yaml existe
if [ ! -f "specs/openapi.yaml" ]; then
    echo "❌ Error: specs/openapi.yaml no encontrado"
    exit 1
fi

# Verifica si ya hay un mock corriendo
if lsof -i :4010 > /dev/null 2>&1; then
    echo "⚠️  Mock server ya está corriendo en puerto 4010"
    echo "💡 Para reiniciar: pkill -f prism && $0"
    exit 0
fi

# Inicia Prism mock en background
echo "🚀 Iniciando Prism mock en http://localhost:4010"
pnpm dlx @stoplight/prism mock specs/openapi.yaml --port 4010 --host 0.0.0.0 &

# Guarda el PID para poder detenerlo después
echo $! > .mock.pid

echo "✅ Mock server iniciado"
echo "📖 Documentación: http://localhost:4010"
echo "🛑 Para detener: pnpm run stop:mock"
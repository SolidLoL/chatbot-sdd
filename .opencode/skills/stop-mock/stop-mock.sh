#!/bin/bash
# .opencode/skills/stop-mock.sh

if [ -f .mock.pid ]; then
    PID=$(cat .mock.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        rm .mock.pid
        echo "✅ Mock server detenido (PID: $PID)"
    else
        rm .mock.pid
        echo "⚠️  Mock server no estaba corriendo (PID file eliminado)"
    fi
else
    echo "⚠️  No se encontró PID file. Intentando matar por nombre..."
    pkill -f "prism mock" && echo "✅ Mock server detenido" || echo "⚠️  Mock server no estaba corriendo"
fi
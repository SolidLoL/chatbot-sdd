#!/bin/bash
# .opencode/skills/validate-contract.sh

set -e

echo "🔍 Validando contrato OpenAPI..."

# 1. Valida sintaxis del YAML
echo "📋 Validando sintaxis YAML..."
pnpm dlx swagger-cli validate specs/openapi.yaml || {
    echo "❌ Error: OpenAPI spec inválida"
    exit 1
}

# 2. Genera modelos Pydantic
echo "🐍 Generando modelos Pydantic..."
bash .opencode/skills/generate-pydantic.sh

# 3. Genera tipos TypeScript
echo "📘 Generando tipos TypeScript..."
pnpm dlx openapi-typescript specs/openapi.yaml -o frontend/src/types/api.ts

# 4. Valida que el backend puede importar los modelos
echo "✅ Validando imports de backend..."
cd backend
python -c "from models import *" || {
    echo "❌ Error: Modelos Pydantic tienen errores de import"
    exit 1
}
cd ..

# 5. Valida que el frontend puede importar los tipos
echo "✅ Validando imports de frontend..."
cd frontend
pnpm exec tsc --noEmit src/types/api.ts || {
    echo "❌ Error: Tipos TypeScript tienen errores"
    exit 1
}
cd ..

echo ""
echo "🎉 Contrato validado exitosamente"
echo "📊 Resumen:"
echo "   - OpenAPI spec: ✅ Válida"
echo "   - Modelos Pydantic: ✅ Generados"
echo "   - Tipos TypeScript: ✅ Generados"
echo "   - Backend imports: ✅ Funcionando"
echo "   - Frontend imports: ✅ Funcionando"
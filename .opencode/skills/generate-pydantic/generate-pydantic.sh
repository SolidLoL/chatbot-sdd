#!/bin/bash
# .opencode/skills/generate-pydantic.sh

set -e

echo "🔄 Generando modelos Pydantic desde OpenAPI..."

# Verifica que openapi.yaml existe
if [ ! -f "specs/openapi.yaml" ]; then
    echo "❌ Error: specs/openapi.yaml no encontrado"
    exit 1
fi

# Crea el directorio si no existe
mkdir -p backend/models

# Genera modelos Pydantic
pnpm dlx datamodel-code-generator \
    --input specs/openapi.yaml \
    --output backend/models/generated.py \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.11 \
    --use-schema-description \
    --use-field-description \
    --reuse-model

# Agrega imports y configuración al inicio del archivo
cat > backend/models/__init__.py << 'EOF'
"""
Modelos Pydantic generados automáticamente desde OpenAPI spec.
NO EDITAR ESTE ARCHIVO MANUALMENTE.
Para regenerar: pnpm run generate:models
"""
from .generated import *
EOF

echo "✅ Modelos Pydantic generados en backend/models/generated.py"
echo "📦 Total de modelos: $(grep -c '^class ' backend/models/generated.py || echo 0)"
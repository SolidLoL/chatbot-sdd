#!/bin/bash
# .opencode/skills/generate-pydantic/generate-pydantic.sh

set -e

echo "🔄 Generando modelos Pydantic desde OpenAPI..."

# Verifica que openapi.yaml existe
if [ ! -f "specs/openapi.yaml" ]; then
    echo "❌ Error: specs/openapi.yaml no encontrado"
    exit 1
fi

# Crea el directorio si no existe
mkdir -p backend/models

# Resuelve el comando datamodel-codegen
if command -v datamodel-codegen &> /dev/null; then
    CMD="datamodel-codegen"
elif python3 -m datamodel_code_generator --help &> /dev/null; then
    CMD="python3 -m datamodel_code_generator"
else
    echo "❌ Error: datamodel-code-generator no está instalado."
    echo "   Instálalo con: pip install datamodel-code-generator"
    exit 1
fi

# Genera modelos Pydantic
$CMD \
    --input specs/openapi.yaml \
    --input-file-type openapi \
    --output backend/models/generated.py \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.11 \
    --use-schema-description \
    --use-field-description \
    --reuse-model \
    --formatters builtin

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
# Variables de entorno — Chatbot SDD

## Backend (`backend/.env`)

| Variable | Tipo | Requerida | Default | Descripción |
|----------|------|-----------|---------|-------------|
| `APP_NAME` | string | No | `Chatbot SDD API` | Nombre del servicio |
| `APP_VERSION` | string | No | `1.0.0` | Versión del servicio |
| `ENVIRONMENT` | string | No | `development` | `development` o `production` |
| `CORS_ORIGINS` | lista JSON | No | `["http://localhost:3000","http://localhost:4010"]` | Orígenes permitidos para CORS |
| `DATABRICKS_HOST` | string | Sí (producción) | `""` | Host del workspace de Databricks (ej: `dbc-xxxxx.cloud.databricks.com`) |
| `DATABRICKS_TOKEN` | string | Sí (producción) | `""` | Token de acceso personal de Databricks |
| `DATABRICKS_WAREHOUSE_ID` | string | No | `""` | ID del warehouse SQL de Databricks |
| `VECTOR_SEARCH_INDEX_NAME` | string | No | `chatbot_docs` | Nombre del índice de Vector Search |
| `VECTOR_SEARCH_ENDPOINT_NAME` | string | No | `vector_search_endpoint` | Nombre del endpoint de Vector Search |
| `MODEL_SERVING_ENDPOINT` | string | No | `""` | Endpoint de Model Serving en Databricks |
| `JWT_SECRET` | string | **Sí** | _generado aleatoriamente_ | Clave secreta para firmar tokens JWT. **Nunca hardcodear.** En producción, generar una clave de 32+ bytes. |
| `JWT_ALGORITHM` | string | No | `HS256` | Algoritmo para JWT |
| `JWT_EXPIRATION_HOURS` | int | No | `24` | Horas de validez del token JWT |
| `RATE_LIMIT_PER_MINUTE` | int | No | `60` | Máximo de peticiones por minuto por IP |
| `RATE_LIMIT_WINDOW_SECONDS` | float | No | `60.0` | Ventana de tiempo para rate limiting (segundos) |

### Ejemplo de `backend/.env` para producción

```ini
ENVIRONMENT=production
DATABRICKS_HOST=dbc-xxxxx.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef
DATABRICKS_WAREHOUSE_ID=abc123def456
VECTOR_SEARCH_INDEX_NAME=chatbot_docs
VECTOR_SEARCH_ENDPOINT_NAME=vector_search_endpoint
MODEL_SERVING_ENDPOINT=databricks-models
JWT_SECRET=<generar con: openssl rand -base64 32>
```

---

## Frontend (`frontend/.env.development` / `frontend/.env.production`)

| Variable | Tipo | Requerida | Default | Descripción |
|----------|------|-----------|---------|-------------|
| `VITE_API_URL` | string | No | `http://localhost:4010` | URL del API (mock o backend real). En producción: `https://api.chatbot-sdd.ezrg.xyz` |
| `VITE_MOCK_ENABLED` | boolean | No | `true` | Muestra indicador visual de mock mode |
| `VITE_DEBUG` | boolean | No | `true` | Logs de desarrollo en consola |

### Recomendaciones de seguridad

1. **JWT_SECRET** debe ser única por entorno y rotada periódicamente. Generar con:
   ```bash
   openssl rand -base64 32
   ```
2. **DATABRICKS_TOKEN** es un secreto sensible. No compartirlo, no commitearlo.
3. En producción, **VITE_API_URL** debe usar HTTPS.
4. Las variables del backend se leen desde `backend/.env` (ignorado por `.gitignore`).
   Las del frontend desde `frontend/.env.production`.

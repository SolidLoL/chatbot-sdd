# Chatbot SDD

Chatbot con RAG (Retrieval-Augmented Generation) usando **Spec-Driven Development**.  
El contrato OpenAPI en `specs/openapi.yaml` es la fuente de verdad única — tipos, mocks, modelos y validación se generan a partir de él.

## Arquitectura

```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│ Frontend │────▶│  Mock    │◀────│  OpenAPI     │
│ (Vite)   │     │ (Prism)  │     │  Spec        │
└──────────┘     └──────────┘     └──────────────┘
       │               │                 │
       │               ▼                 │
       │         ┌──────────┐            │
       └────────▶│ Backend  │────────────┘
                 │(FastAPI) │
                 └──────────┘
                      │
                      ▼
              ┌──────────────┐
              │  Databricks  │
              │  (Vector     │
              │   Search +   │
              │   FM API)    │
              └──────────────┘
```

- **Frontend**: React + TypeScript + Vite. Consume el API vía SSE (Server-Sent Events).
- **Mock**: Servidor Prism que simula el API a partir del spec. Ideal para desarrollo frontend sin backend real.
- **Backend**: FastAPI (scaffold, en progreso). Conecta con Databricks para RAG.
- **Spec**: Archivo OpenAPI 3.1 que define todos los endpoints, schemas y ejemplos.

## Directorios

```
chatbot-sdd/
├── specs/
│   └── openapi.yaml              ← Contrato API (fuente de verdad)
│
├── frontend/                     ← App React + TypeScript + Vite
│   ├── src/
│   │   ├── components/
│   │   │   └── chat/
│   │   │       ├── ChatWindow.tsx      ← Ventana principal del chat
│   │   │       ├── MessageBubble.tsx   ← Burbuja de mensaje (user/assistant)
│   │   │       ├── MessageInput.tsx    ← Input para escribir mensajes
│   │   │       └── CitationCard.tsx    ← Carta de fuente RAG consultada
│   │   ├── hooks/
│   │   │   └── useChat.ts             ← Hook de chat con streaming SSE
│   │   ├── lib/
│   │   │   ├── api-client.ts          ← Cliente Axios configurado
│   │   │   ├── sse-client.ts          ← Cliente SSE (AsyncGenerator)
│   │   │   └── query-client.ts        ← TanStack Query client
│   │   ├── types/
│   │   │   └── api.ts                 ← Tipos generados del spec
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css                  ← Tailwind v4 + tema custom
│   ├── .env.development
│   ├── .env.production
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig*.json
│
├── backend/                      ← FastAPI (scaffold — WIP)
│   └── pyproject.toml
│
├── .opencode/
│   └── skills/                   ← Scripts de generación y validación
│       ├── generate-mocks/       ←   Mock API con Prism
│       ├── generate-pydantic/    ←   Modelos Pydantic desde el spec
│       ├── generate-types/       ←   Tipos TypeScript desde el spec
│       ├── run-evaluation/       ←   Evaluación de calidad del chatbot
│       ├── start-mock/           ←   Iniciar mock server
│       ├── stop-mock/            ←   Detener mock server
│       └── validate-contract/    ←   Contract testing backend vs spec
│
├── docker-compose.yml            ← mock (4010) + backend (8000) + frontend (3000)
└── README.md
```

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | React 19, TypeScript 6, Vite 8, Tailwind CSS v4 |
| Estado | TanStack Query, Zustand |
| Backend | Python 3.11, FastAPI, Pydantic, Uvicorn |
| Mock | Stoplight Prism 4 |
| Infra | Docker, Docker Compose |
| DB / AI | Databricks (Vector Search + Foundation Model APIs) |

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/v1/chat` | Enviar mensaje y recibir respuesta en streaming SSE |
| `GET` | `/v1/sessions` | Listar sesiones del usuario |
| `GET` | `/v1/sessions/{session_id}` | Obtener sesión con historial completo |
| `DELETE` | `/v1/sessions/{session_id}` | Eliminar sesión |
| `POST` | `/v1/feedback` | Calificar una respuesta del chatbot |
| `GET` | `/v1/health` | Health check del servicio |

### Streaming SSE (`POST /v1/chat`)

El endpoint devuelve eventos `text/event-stream` con los siguientes tipos:

| Evento | Descripción |
|---|---|
| `thinking` | Proceso de razonamiento (opcional) |
| `token` | Token de texto generado |
| `citation` | Fuente RAG consultada |
| `done` | Fin del stream (incluye `message_id`) |
| `error` | Error durante el stream |

## Cómo empezar

### Opción A — Todo con Docker

```bash
docker compose up
# → mock en http://localhost:4010
# → backend en http://localhost:8000
# → frontend en http://localhost:3000
```

### Opción B — Desarrollo frontend (con mock)

```bash
# 1. Iniciar mock
docker compose up mock -d

# 2. Frontend
cd frontend
pnpm install
pnpm dev
# → http://localhost:3000
```

### Opción C — Desarrollo backend

```bash
# 1. Iniciar mock
docker compose up mock -d

# 2. Backend (manual)
cd backend
pip install fastapi uvicorn[standard] pydantic
uvicorn main:app --reload --port 8000
```

### Prerrequisitos

- **Node.js** 20+ y **pnpm**
- **Python** 3.11+
- **Docker** y **Docker Compose** (para el mock server)
- Acceso a **Databricks** (para backend en producción)

## Variables de Entorno

### Frontend (`.env.development` / `.env.production`)

| Variable | Default | Descripción |
|---|---|---|
| `VITE_API_URL` | `http://localhost:4010` | URL del API (mock o backend) |
| `VITE_MOCK_ENABLED` | `true` | Mostrar indicadores visuales de mock |
| `VITE_DEBUG` | `true` | Logs de desarrollo |

### Backend

| Variable | Descripción |
|---|---|
| `DATABRICKS_HOST` | Host del workspace de Databricks |
| `DATABRICKS_TOKEN` | Token de acceso a Databricks |
| `ENVIRONMENT` | `development` / `production` |

## Flujo de trabajo SDD

```
1. Editar specs/openapi.yaml
         │
         ▼
2. Generar tipos/mocks/modelos
   ┌─────────────────────────────┐
   │ pnpm generate:types         │  → frontend/src/types/api.ts
   │ pnpm generate:mock          │  → mock server via Prism
   │ cd backend && generate-models│ → modelos Pydantic (pendiente)
   └─────────────────────────────┘
         │
         ▼
3. Implementar backend (FastAPI)
         │
         ▼
4. Validar contrato
   ┌─────────────────────────────┐
   │ pnpm validate               │  → backend vs spec
   └─────────────────────────────┘
         │
         ▼
5. Consumir desde frontend
```

## Comandos Disponibles

### Frontend (`cd frontend`)

| Comando | Descripción |
|---|---|
| `pnpm dev` | Iniciar servidor de desarrollo |
| `pnpm build` | Compilar TypeScript + Vite |
| `pnpm lint` | Ejecutar ESLint |
| `pnpm preview` | Preview del build de producción |
| `pnpm generate:types` | Generar tipos TS desde `specs/openapi.yaml` |
| `pnpm validate` | Contract testing backend vs spec |

### Backend (`cd backend`)

| Comando | Descripción |
|---|---|
| `generate-models` | Generar modelos Pydantic desde `specs/openapi.yaml` |
| `validate` | Contract testing contra el API desplegada |

## Estructura del Proyecto (explicada)

### `specs/`
Archivo OpenAPI 3.1 que define toda la API. Es la fuente de verdad. Cualquier cambio en el comportamiento del API empieza aquí.

### `frontend/src/lib/`
- **`api-client.ts`**: Cliente Axios con interceptores para auth token y redirección en 401.
- **`sse-client.ts`**: Cliente SSE que consume `POST /v1/chat` como `AsyncGenerator`. Emite eventos `token`, `citation`, `thinking`, `done`, `error`.
- **`query-client.ts`**: Cliente de TanStack Query con configuración por defecto (stale time 5 min, 1 retry).

### `frontend/src/hooks/`
- **`useChat.ts`**: Hook que orquesta el streaming SSE. Retorna `sendMessage`, `isStreaming`, `currentMessage` (texto acumulado), `citations` (array de fuentes) y `error`.

### `frontend/src/components/chat/`
- **`ChatWindow.tsx`**: Contenedor principal. Maneja el estado de mensajes (local), integra `useChat` y renderiza `MessageBubble` + `MessageInput`.
- **`MessageBubble.tsx`**: Burbuja de mensaje. Renderiza markdown con `react-markdown` y opcionalmente las citas RAG.
- **`MessageInput.tsx`**: Input de texto con estado local y callback `onSend`.
- **`CitationCard.tsx`**: Carta individual de fuente consultada. Muestra título (linkeado si tiene URL), snippet y barra de relevancia.

### `.opencode/skills/`
Scripts shell que automatizan el pipeline SDD. Se ejecutan desde la raíz del proyecto o vía targets en `package.json` / `pyproject.toml`.

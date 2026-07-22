# Project Constitution

> Governing principles, values, and development guidelines for chatbot-sdd.

## Mission & Vision

Build a secure, streaming-capable chatbot backend with a modern React frontend, leveraging Databricks for AI inference. The project serves as a reference architecture for contract-first API development with OpenAPI 3.1, FastAPI, and type-safe frontends.

Long-term vision: a production-grade chatbot platform with evaluation pipelines, observability, and multi-provider AI support.

## Core Values

- **Balance pragmático** — calidad y velocidad según el contexto. No sobre-diseñar, no apresurar.
- **Contract-first** — OpenAPI spec es la fuente de verdad. Todo cambio de API empieza por la spec.
- **Documentado** — documentación paralela al código, actualizada siempre. READMEs, ADRs, CONSTITUTION.md.
- **Security by design** — JWT auth, validación de entrada, logging estructurado, sin secretos en código.
- **Iterar con feedback** — releases pequeños, evaluación continua, ajustar basado en resultados.

## Architecture Principles

- **OpenAPI-first**: toda interfaz entre frontend y backend se define en `specs/openapi.yaml`. Los tipos se generan desde allí.
- **Separation of concerns**: API layer (routes) → Service layer (business logic) → Client layer (Databricks SDK, etc.). Cada capa tiene una responsabilidad única.
- **Streaming-first**: las respuestas de AI usan SSE (Server-Sent Events) para experiencia en tiempo real. El frontend consume el stream via `EventSource`.
- **Stateless backend**: el estado de sesión se persiste en servicios externos (Databricks), no en memoria del servidor. Escalamiento horizontal directo.
- **Fail fast**: validación de entrada en los borders del sistema (Pydantic en API, tipos en frontend). Errores tempranos, mensajes claros.

## Tech Stack Rationale

| Layer | Choice | Rationale |
|---|---|---|
| Backend framework | FastAPI (Python) | Async-native, generación automática de OpenAPI, validación con Pydantic v2 |
| Frontend framework | React + TypeScript | Tipado fuerte, ecosistema maduro, soporte SSE nativo |
| AI provider | Databricks SDK | Proveedor principal de inferencia, vector search, session management |
| Auth | JWT (python-jose + passlib) | Stateless, estándar, sin dependencia externa de sesión |
| API spec | OpenAPI 3.1 (YAML) | Contract-first, language-agnostic, tooling maduro |
| Streaming | SSE via sse-starlette | Protocolo simple sobre HTTP, sin necesidad de WebSocket |
| Logging | structlog | Logging estructurado con contexto, bindings por request |
| Config | pydantic-settings | Validación de entorno en startup, dotenv para dev |
| Testing | pytest + pytest-asyncio | Async support nativo, fixtures, integración con FastAPI TestClient |

## Code Standards

- **Type hints everywhere**: Python `mypy strict`, TypeScript `strict: true`. Sin excepciones.
- **Naming**: `snake_case` (Python), `camelCase` (TypeScript), `PascalCase` (componentes/clases).
- **Imports**: stdlib → third-party → local, agrupados y ordenados (isort / eslint import ordering).
- **Max line length**: 100 caracteres.
- **Docstrings**: solo en APIs públicas, estilo Google.
- **No commented-out code**: se elimina, no se comenta. git history existe por una razón.
- **Error handling**: errores de dominio con códigos HTTP semanticos (4xx/5xx), logs estructurados con contexto.

## Testing Philosophy

- **Mínima pero estratégica**: tests solo para lógica crítica y bordes del sistema.
- **Contract tests**: validación de que backend cumple la OpenAPI spec (pytest + schemathesis o similar).
- **Integration tests**: rutas críticas (chat, auth, sessions) con FastAPI TestClient.
- **AI evaluation**: suite separada con golden dataset para calidad de respuestas (no en CI principal).
- **No se requiere cobertura numérica obligatoria** — priorizar calidad de tests sobre cantidad.

## Development Workflow

- **Branch model**: `main` (estable) + feature branches desde `main`. Naming: `feat/<name>`, `fix/<name>`, `chore/<name>`.
- **Commits semánticos**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`. Cuerpo opcional pero descriptivo.
- **PR flow**: feature branch → CI (lint + test) → review → merge a `main`. Sin commits directos a `main`.
- **Spec evolution**: todo cambio funcional sigue el workflow speckit:
  `specify` → `plan` → `tasks` → `implement` → `converge`
- **Regeneración**: después de cambiar OpenAPI spec, regenerar tipos: `generate-types` (frontend) y `generate-pydantic` (backend).

## Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-07-21 | speckit workflow | Estructurar el desarrollo con skills secuenciales: constitution → specify → plan → tasks → implement → converge |
| 2026-07-21 | Contract-first con OpenAPI 3.1 | Fuente de verdad única para frontend y backend, genera tipos automáticamente |
| 2026-07-21 | Streaming con SSE | Protocolo simple, unidireccional, suficiente para respuestas de AI. No requiere WebSocket |

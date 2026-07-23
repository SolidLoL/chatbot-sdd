# PostgreSQL Persistence for Sessions & Messages

## User Stories

**US-01** — Como usuario, quiero que mis conversaciones persistan al recargar la página o reiniciar el servidor.

**US-02** — Como usuario, quiero poder listar mis sesiones anteriores para retomar conversaciones pasadas.

**US-03** — Como desarrollador, quiero migraciones versionadas para evolucionar el schema sin perder datos.

## Acceptance Criteria

| ID | Criterio | Estado |
|---|---|---|
| AC-01 | Sesiones y mensajes se almacenan en PostgreSQL | ✅ |
| AC-02 | Al reiniciar el backend, las sesiones anteriores siguen disponibles | ✅ |
| AC-03 | `GET /v1/sessions` retorna sesiones desde la DB | ✅ |
| AC-04 | `DELETE /v1/sessions/{id}` elimina sesión + mensajes (cascade) | ✅ |
| AC-05 | Las migraciones se ejecutan automáticamente al iniciar el backend | ✅ |
| AC-06 | Postgres + pgadmin disponibles via docker-compose | ✅ |
| AC-07 | En desarrollo sin Docker, se puede usar DATABASE_URL de .env | ✅ |

## Schema

```sql
CREATE TABLE sessions (
    id         TEXT PRIMARY KEY,
    user_id    TEXT NOT NULL,
    title      TEXT NOT NULL DEFAULT 'Nueva conversación',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE messages (
    id          TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role        TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content     TEXT NOT NULL,
    citations   JSONB NOT NULL DEFAULT '[]',
    metadata    JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_updated_at ON sessions(updated_at DESC);
```

## Architecture

### New Files

| File | Purpose |
|---|---|
| `backend/app/core/database.py` | asyncpg connection pool singleton |
| `backend/app/repositories/session_repo.py` | CRUD sessions against PostgreSQL |
| `backend/app/repositories/message_repo.py` | CRUD messages against PostgreSQL |
| `backend/alembic.ini` | Alembic configuration |
| `backend/migrations/env.py` | Alembic environment (inline config import) |
| `backend/migrations/versions/001_initial.py` | Initial schema migration |

### Modified Files

| File | Change |
|---|---|
| `backend/requirements.txt` | + `asyncpg`, + `alembic` |
| `backend/app/core/config.py` | + `DATABASE_URL: str` |
| `backend/app/services/session_service.py` | Replace in-memory dict with repos |
| `backend/app/main.py` | Init/close DB pool in lifespan |
| `docker-compose.yml` | + postgres + pgadmin services |

## Data Flow

```
POST /v1/chat
  → chat.py
  → session_service.create_session(user_id)
     → session_repo.create(user_id)       -- INSERT INTO sessions
  → session_service.add_message(...)
     → message_repo.add(...)              -- INSERT INTO messages

GET /v1/sessions
  → session_service.list_sessions(user_id)
     → session_repo.list_by_user(user_id, limit, offset)

GET /v1/sessions/{id}
  → session_service.get_session(id)
     → session_repo.get_by_id(id)
     → message_repo.list_by_session(id)

DELETE /v1/sessions/{id}
  → session_service.delete_session(id)
     → message_repo.delete_by_session(id)
     → session_repo.delete(id)
```

## Configuration

```env
DATABASE_URL=postgresql+asyncpg://chatbot:chatbot@localhost:5432/chatbot
```

For Docker: `postgresql+asyncpg://chatbot:chatbot@postgres:5432/chatbot`

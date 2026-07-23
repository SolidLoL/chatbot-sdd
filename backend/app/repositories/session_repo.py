from typing import Optional
from datetime import datetime, timezone
import uuid
import structlog

logger = structlog.get_logger()


class SessionRepo:
    def __init__(self, pool):
        self._pool = pool

    async def create(self, user_id: str) -> str:
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO sessions (id, user_id, title, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                """,
                session_id, user_id, "Nueva conversación", now, now,
            )
        logger.info("Session created", session_id=session_id, user_id=user_id)
        return session_id

    async def get_by_id(self, session_id: str) -> Optional[dict]:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, user_id, title, created_at, updated_at FROM sessions WHERE id = $1",
                session_id,
            )
        if row is None:
            return None
        return dict(row)

    async def list_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[dict]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, user_id, title, created_at, updated_at
                FROM sessions
                WHERE user_id = $1
                ORDER BY updated_at DESC
                LIMIT $2 OFFSET $3
                """,
                user_id, limit, offset,
            )
        return [dict(r) for r in rows]

    async def update_title(self, session_id: str, title: str):
        now = datetime.now(timezone.utc).isoformat()
        async with self._pool.acquire() as conn:
            await conn.execute(
                "UPDATE sessions SET title = $1, updated_at = $2 WHERE id = $3",
                title, now, session_id,
            )

    async def touch(self, session_id: str):
        now = datetime.now(timezone.utc).isoformat()
        async with self._pool.acquire() as conn:
            await conn.execute(
                "UPDATE sessions SET updated_at = $1 WHERE id = $2",
                now, session_id,
            )

    async def delete(self, session_id: str) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM sessions WHERE id = $1",
                session_id,
            )
        return result != "DELETE 0"

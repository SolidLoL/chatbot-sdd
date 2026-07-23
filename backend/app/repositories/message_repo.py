import json
from typing import Optional
from datetime import datetime, timezone
import uuid


class MessageRepo:
    def __init__(self, pool):
        self._pool = pool

    async def add(
        self,
        session_id: str,
        role: str,
        content: str,
        citations: Optional[list[dict]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO messages (id, session_id, role, content, citations, metadata, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                msg_id, session_id, role, content,
                json.dumps(citations or []),
                json.dumps(metadata or {}),
                now,
            )
        return {
            "id": msg_id,
            "role": role,
            "content": content,
            "citations": citations or [],
            "metadata": metadata or {},
            "created_at": now,
        }

    async def list_by_session(self, session_id: str) -> list[dict]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, session_id, role, content, citations, metadata, created_at
                FROM messages
                WHERE session_id = $1
                ORDER BY created_at ASC
                """,
                session_id,
            )
        result = []
        for r in rows:
            d = dict(r)
            d["citations"] = json.loads(d.get("citations") or "[]")
            d["metadata"] = json.loads(d.get("metadata") or "{}")
            result.append(d)
        return result

    async def delete_by_session(self, session_id: str):
        async with self._pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM messages WHERE session_id = $1",
                session_id,
            )

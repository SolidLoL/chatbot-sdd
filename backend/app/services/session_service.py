from typing import Optional
from datetime import datetime, timezone
import uuid
import structlog

from app.repositories.session_repo import SessionRepo
from app.repositories.message_repo import MessageRepo

logger = structlog.get_logger()

# In-memory fallback for dev/test when no DB pool is available
_sessions: dict = {}


class SessionService:
    def __init__(self, pool=None):
        self._pool = pool
        if pool is not None:
            self._sessions = SessionRepo(pool)
            self._messages = MessageRepo(pool)
        else:
            self._sessions = None
            self._messages = None

    async def create_session(self, user_id: str) -> str:
        if self._pool:
            return await self._sessions.create(user_id)
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        _sessions[session_id] = {
            "id": session_id,
            "user_id": user_id,
            "title": "Nueva conversación",
            "messages": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        logger.info("Session created (memory)", session_id=session_id, user_id=user_id)
        return session_id

    async def get_session(self, session_id: str) -> Optional[dict]:
        if self._pool:
            session = await self._sessions.get_by_id(session_id)
            if session is None:
                return None
            messages = await self._messages.list_by_session(session_id)
            session["messages"] = messages
            return session
        return _sessions.get(session_id)

    async def list_sessions(self, user_id: str, limit: int = 20, offset: int = 0) -> list[dict]:
        if self._pool:
            return await self._sessions.list_by_user(user_id, limit, offset)
        user_sessions = [s for s in _sessions.values() if s["user_id"] == user_id]
        return user_sessions[offset:offset + limit]

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        citations: Optional[list[dict]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        if self._pool:
            session = await self._sessions.get_by_id(session_id)
            if session is None:
                raise ValueError(f"Session {session_id} not found")
            message = await self._messages.add(
                session_id=session_id, role=role, content=content,
                citations=citations, metadata=metadata,
            )
            await self._sessions.touch(session_id)
            if role == "user":
                title = content[:50] + ("..." if len(content) > 50 else "")
                await self._sessions.update_title(session_id, title)
            return message

        if session_id not in _sessions:
            raise ValueError(f"Session {session_id} not found")
        message = {
            "id": f"msg_{uuid.uuid4().hex[:12]}",
            "role": role,
            "content": content,
            "citations": citations or [],
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _sessions[session_id]["messages"].append(message)
        _sessions[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
        if len(_sessions[session_id]["messages"]) == 1 and role == "user":
            _sessions[session_id]["title"] = content[:50] + "..."
        return message

    async def delete_session(self, session_id: str) -> bool:
        if self._pool:
            await self._messages.delete_by_session(session_id)
            return await self._sessions.delete(session_id)
        if session_id in _sessions:
            del _sessions[session_id]
            return True
        return False

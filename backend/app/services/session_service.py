from typing import Optional, List
import uuid
from datetime import datetime
import structlog

logger = structlog.get_logger()

# Estado compartido entre instancias (singleton a nivel de módulo)
_sessions: dict = {}


class SessionService:
    """Gestión de sesiones de chat (mock por ahora)"""

    @property
    def sessions(self):
        return _sessions

    async def create_session(self, user_id: str) -> str:
        """Crea una nueva sesión"""
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        _sessions[session_id] = {
            "id": session_id,
            "user_id": user_id,
            "title": "Nueva conversación",
            "messages": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        logger.info("Session created", session_id=session_id, user_id=user_id)
        return session_id

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Obtiene una sesión"""
        return _sessions.get(session_id)

    async def list_sessions(self, user_id: str, limit: int = 20, offset: int = 0) -> List[dict]:
        """Lista sesiones del usuario"""
        user_sessions = [
            s for s in _sessions.values()
            if s["user_id"] == user_id
        ]
        return user_sessions[offset:offset + limit]

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        citations: Optional[List[dict]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Agrega un mensaje a la sesión"""
        if session_id not in _sessions:
            raise ValueError(f"Session {session_id} not found")

        message = {
            "id": f"msg_{uuid.uuid4().hex[:12]}",
            "role": role,
            "content": content,
            "citations": citations or [],
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }

        _sessions[session_id]["messages"].append(message)
        _sessions[session_id]["updated_at"] = datetime.utcnow().isoformat()

        # Actualizar título si es el primer mensaje
        if len(_sessions[session_id]["messages"]) == 1 and role == "user":
            _sessions[session_id]["title"] = content[:50] + "..."

        return message

    async def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión"""
        if session_id in _sessions:
            del _sessions[session_id]
            return True
        return False

from app.services.chat_service import ChatService
from app.services.session_service import SessionService

# Singleton para el servicio de sesiones (en memoria para desarrollo)
_session_service_instance = SessionService()


def get_chat_service() -> ChatService:
    return ChatService()


def get_session_service() -> SessionService:
    return _session_service_instance

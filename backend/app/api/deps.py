from app.services.chat_service import ChatService
from app.services.session_service import SessionService


def get_chat_service() -> ChatService:
    return ChatService()


def get_session_service() -> SessionService:
    return SessionService()
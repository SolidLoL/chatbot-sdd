import structlog

logger = structlog.get_logger()


def get_chat_service():
    from app.services.chat_service import ChatService
    return ChatService()


async def get_session_service():
    from app.services.session_service import SessionService
    try:
        from app.core.database import get_pool
        pool = await get_pool()
        return SessionService(pool)
    except Exception as e:
        logger.warning("Database unavailable, using in-memory fallback", error=str(e))
        return SessionService(pool=None)

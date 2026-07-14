from fastapi import APIRouter, Depends, HTTPException, status
from sse_starlette.sse import EventSourceResponse
import structlog
from typing import AsyncGenerator

from app.models.generated import ChatRequest, Message, Citation
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.services.session_service import SessionService

logger = structlog.get_logger()
router = APIRouter()


@router.post("/chat")
async def create_chat_message(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(),
    session_service: SessionService = Depends(),
):
    """
    Envía un mensaje y recibe respuesta en streaming SSE.
    
    Eventos SSE:
    - thinking: Proceso de razonamiento
    - citation: Fuente RAG consultada
    - token: Token de texto generado
    - done: Fin del stream con metadatos
    - error: Error durante el stream
    """
    logger.info(
        "Chat request received",
        user_id=current_user["user_id"],
        session_id=request.session_id,
        message_length=len(request.message),
    )
    
    # Crear o obtener sesión
    session_id = request.session_id or await session_service.create_session(
        user_id=current_user["user_id"]
    )
    
    # Guardar mensaje del usuario
    user_message = await session_service.add_message(
        session_id=session_id,
        role="user",
        content=request.message,
    )
    
    if request.stream:
        # Streaming SSE
        return EventSourceResponse(
            stream_chat_response(
                session_id=session_id,
                message=request.message,
                chat_service=chat_service,
                session_service=session_service,
            )
        )
    else:
        # Respuesta completa (no streaming)
        response = await chat_service.generate_response(
            session_id=session_id,
            message=request.message,
        )
        
        # Guardar respuesta del asistente
        assistant_message = await session_service.add_message(
            session_id=session_id,
            role="assistant",
            content=response["content"],
            citations=response.get("citations"),
            metadata=response.get("metadata"),
        )
        
        return assistant_message


async def stream_chat_response(
    session_id: str,
    message: str,
    chat_service: ChatService,
    session_service: SessionService,
) -> AsyncGenerator:
    """Genera eventos SSE para el stream de chat"""
    full_response = ""
    citations = []
    
    try:
        # Evento de pensamiento
        yield {
            "event": "thinking",
            "data": {"content": "Procesando tu pregunta..."}
        }
        
        # Generar respuesta token por token
        async for event in chat_service.stream_response(
            session_id=session_id,
            message=message,
        ):
            if event["type"] == "token":
                full_response += event["data"]["content"]
                yield {"event": "token", "data": event["data"]}
            
            elif event["type"] == "citation":
                citations.append(event["data"])
                yield {"event": "citation", "data": event["data"]}
        
        # Guardar mensaje completo en la sesión
        assistant_message = await session_service.add_message(
            session_id=session_id,
            role="assistant",
            content=full_response,
            citations=citations,
        )
        
        # Evento de finalización
        yield {
            "event": "done",
            "data": {
                "message_id": assistant_message["id"],
                "session_id": session_id,
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }
        }
    
    except Exception as e:
        logger.error("Error during chat streaming", error=str(e))
        yield {
            "event": "error",
            "data": {"message": "Error al generar respuesta"}
        }
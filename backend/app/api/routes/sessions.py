from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import structlog

from app.core.security import get_current_user
from app.api.deps import get_session_service
from app.services.session_service import SessionService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/sessions")
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    session_service: SessionService = Depends(),
):
    """Lista sesiones del usuario"""
    sessions = await session_service.list_sessions(
        user_id=current_user["user_id"],
        limit=limit,
        offset=offset,
    )
    
    return {
        "sessions": sessions,
        "total": len(sessions),
        "limit": limit,
        "offset": offset,
    }


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    session_service: SessionService = Depends(get_session_service),
):
    """Obtiene una sesión con su historial"""
    session = await session_service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    
    if session["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta sesión",
        )
    
    return session


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    session_service: SessionService = Depends(get_session_service),
):
    """Elimina una sesión"""
    session = await session_service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada",
        )
    
    if session["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta sesión",
        )
    
    await session_service.delete_session(session_id)
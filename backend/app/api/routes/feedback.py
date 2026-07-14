from fastapi import APIRouter, Depends, HTTPException, status
import structlog

from app.models.generated import FeedbackRequest, FeedbackResponse
from app.core.security import get_current_user

logger = structlog.get_logger()
router = APIRouter()


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    request: FeedbackRequest,
    current_user: dict = Depends(get_current_user),
):
    """Registra feedback sobre una respuesta"""
    logger.info(
        "Feedback received",
        user_id=current_user["user_id"],
        message_id=request.message_id,
        rating=request.rating,
    )
    
    # TODO: Guardar en base de datos para evaluación continua
    
    return FeedbackResponse(
        id=f"fb_{request.message_id}",
        status="registered",
    )
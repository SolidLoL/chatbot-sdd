from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check del servicio"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "dependencies": {
            "databricks": "up",  # TODO: Verificar conexión real
            "vector_search": "up",  # TODO: Verificar conexión real
        }
    }
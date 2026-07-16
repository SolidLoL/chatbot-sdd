from fastapi import APIRouter, HTTPException
import httpx
import structlog

from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check del servicio con verificación real de dependencias"""
    status = "healthy"
    
    # Verificar Databricks (si está configurado)
    databricks_status = "up"
    if settings.DATABRICKS_HOST:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"https://{settings.DATABRICKS_HOST}/api/2.1/jobs/list-run",
                    headers={"Authorization": f"Bearer {settings.DATABRICKS_TOKEN}"}
                )
                databricks_status = "up" if resp.status_code == 200 else "down"
        except Exception:
            databricks_status = "down"
    
    # Verificar endpoint de vector search (si está configurado)
    vector_search_status = "up"
    if settings.VECTOR_SEARCH_ENDPOINT_NAME:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"https://{settings.DATABRICKS_HOST}/serving-endpoints/{settings.VECTOR_SEARCH_ENDPOINT_NAME}/invocations",
                    headers={"Authorization": f"Bearer {settings.DATABRICKS_TOKEN}"}
                )
                vector_search_status = "up" if resp.status_code == 200 else "down"
        except Exception:
            vector_search_status = "down"
    
    return {
        "status": status,
        "version": settings.APP_VERSION,
        "dependencies": {
            "databricks": databricks_status,
            "vector_search": vector_search_status,
        }
    }
    }
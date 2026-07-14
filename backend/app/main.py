from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.api.routes import chat, sessions, feedback, system
from app.core.config import settings
from app.core.logging import setup_logging

# Configurar logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    logger.info("Starting Chatbot SDD API")
    yield
    logger.info("Shutting down Chatbot SDD API")


# Crear app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Chatbot API con RAG usando Spec-Driven Development",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(sessions.router, prefix="/v1", tags=["sessions"])
app.include_router(feedback.router, prefix="/v1", tags=["feedback"])
app.include_router(system.router, prefix="/v1", tags=["system"])


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid
import structlog

from app.api.routes import chat, sessions, feedback, system
from app.core.auth import setup as auth_setup, teardown as auth_teardown
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import get_pool, close_pool

setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Chatbot SDD API")
    await auth_setup()
    await get_pool()
    yield
    await close_pool()
    await auth_teardown()
    logger.info("Shutting down Chatbot SDD API")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Chatbot API con RAG usando Spec-Driven Development",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = uuid.uuid4().hex[:12]
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )
    logger.info("Request started")
    response = await call_next(request)
    structlog.contextvars.bind_contextvars(status_code=response.status_code)
    logger.info("Request completed")
    structlog.contextvars.clear_contextvars()
    return response


from collections import defaultdict
import time

rate_limit_store = defaultdict(list)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    rate_limit_store[client_ip] = [
        ts for ts in rate_limit_store[client_ip]
        if now - ts < settings.RATE_LIMIT_WINDOW_SECONDS
    ]

    if len(rate_limit_store[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        reset_time = int(now + settings.RATE_LIMIT_WINDOW_SECONDS)
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Has excedido el límite de peticiones",
                "code": "RATE_LIMITED",
                "retry_after": reset_time,
            },
            headers={
                "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_time),
            },
        )

    rate_limit_store[client_ip].append(now)
    response = await call_next(request)

    if response.status_code != 429:
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, settings.RATE_LIMIT_PER_MINUTE - len(rate_limit_store[client_ip]))
        )
        response.headers["X-RateLimit-Reset"] = str(int(now + settings.RATE_LIMIT_WINDOW_SECONDS))

    return response


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

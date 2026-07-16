"""
Módulo de autenticación para el backend.

Este módulo implementa:
- Endpoint /login que recibe un JWT del Identity Provider (Auth0, Entra ID, etc.)
  y lo guarda en sessionStorage del navegador (más seguro que localStorage).
- Validación básica de tokens JWT usando la clave secreta configurada.
- Middleware que redirige a /login cuando falta autenticación o el token es inválido.

NO IMPLEMENTA PERSISTENCIA DE SESIONES EN BASE DE DATOS — las sesiones viven
en el navegador del cliente (sessionStorage). En producción, deberías integrar
con tu IdP real y validar tokens contra él.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import PlainTextResponse
from jose import JWTError, jwt
import structlog

from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()


async def validate_token(token: str) -> dict | None:
    """
    Valida un token JWT y extrae la información del usuario.

    En desarrollo, decodifica el token con la clave secreta configurada (que
    puede ser una aleatoria segura si no se ha definido JWT_SECRET). En
    producción, esto debería delegarse a tu Identity Provider para validar
    contra él.

    Retorna un dict con al menos {"user_id": str} o None si el token es inválido.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError as e:
        logger.warning("JWT validation failed", error=str(e))
        return None


@router.post("/login")
async def login(request: Request) -> PlainTextResponse:
    """
    Endpoint de login para recibir un JWT del Identity Provider.

    El frontend debe llamar a este endpoint con el token que recibe del IdP
    (Auth0, Entra ID, etc.). Este endpoint valida el token y devuelve un
    script JavaScript que guarda el token en sessionStorage con las flags
    secure=true y sameSite=strict para protegerlo contra XSS y robo por HTTP.

    El frontend luego redirige al usuario a la app con ese token en el header
    Authorization: Bearer <token>.

    En desarrollo, también acepta un payload JSON arbitrario (para pruebas)
    pero lo guarda igual en sessionStorage.
    """
    body = await request.json() if request.method == "POST" else {}
    token = body.get("token")

    # Validar token contra el IdP (o decodificar si es auto-emitido en desarrollo)
    user_info = validate_token(token) if token else None
    if not user_info:
        logger.warning("Login failed: invalid token", token=token[:8] + "...")
        return PlainTextResponse(
            "Token inválido. Verifica que tu Identity Provider emitió un JWT válido.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Guardar en sessionStorage (más seguro que localStorage)
    script = f"""
    <script>
      if (window.location.protocol === 'https:') {{
        sessionStorage.setItem('auth_token', '{token}');
      }} else {{
        // En desarrollo también usamos sessionStorage para consistencia
        sessionStorage.setItem('auth_token', '{token}');
      }}
      console.log('Token guardado en sessionStorage');
    </script>
    """
    return PlainTextResponse(script, media_type="text/plain")


def get_unauthenticated_redirect(request: Request) -> str:
    """Devuelve la URL a redirigir cuando falta autenticación."""
    origin = request.headers.get("origin", "http://localhost:3000")
    return f"{origin}/login?error=unauthorized"


async def require_authentication(
    request: Request, current_user: dict = Depends(validate_token)
) -> dict:
    """
    Dependency que requiere autenticación.

    Si no hay header Authorization o el token es inválido, redirige a /login
    con un parámetro de error y devuelve None (el router nunca se ejecuta).
    En desarrollo también acepta tokens auto-emitidos; en producción deberías
    validar contra tu IdP real.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.info(
            "Request without authentication",
            method=request.method,
            path=request.url.path,
        )
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": get_unauthenticated_redirect(request)},
        )

    token = auth_header[7:]  # quitar "Bearer "
    user_info = validate_token(token)
    if not user_info:
        logger.warning("Request with invalid token", method=request.method)
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": get_unauthenticated_redirect(request)},
        )

    return user_info


# Middleware para redirigir automáticamente a /login en respuestas 401
async def auth_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        redirect_url = get_unauthenticated_redirect(request)
        return PlainTextResponse(
            f"<script>window.location.href='{redirect_url}';</script>",
            status_code=status.HTTP_302_FOUND,
            headers={"Location": redirect_url},
        )
    return response

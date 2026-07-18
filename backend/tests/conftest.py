import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import get_current_user


async def override_get_current_user():
    """Override de autenticación para tests — devuelve un usuario mock"""
    return {"user_id": "test_user_123", "email": "test@example.com"}


@pytest.fixture
def client():
    """Cliente HTTP asíncrono con la app de FastAPI"""
    app.dependency_overrides[get_current_user] = override_get_current_user
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    return client


@pytest.fixture(autouse=True)
def clean_dependency_overrides():
    """Limpia los overrides después de cada test"""
    yield
    app.dependency_overrides.clear()

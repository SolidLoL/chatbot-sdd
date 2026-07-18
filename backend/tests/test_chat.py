import pytest


@pytest.mark.asyncio
async def test_chat_stream_false(client):
    """POST /v1/chat con stream=false devuelve respuesta JSON completa"""
    payload = {
        "session_id": None,
        "message": "¿Cómo configuro Vector Search?",
        "stream": False,
    }
    response = await client.post("/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["role"] == "assistant"
    assert "content" in data
    assert "citations" in data


@pytest.mark.asyncio
async def test_health_check(client):
    """GET /v1/health devuelve estado del servicio"""
    response = await client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded", "unhealthy")
    assert "version" in data
    assert "dependencies" in data
    assert "databricks" in data["dependencies"]
    assert "vector_search" in data["dependencies"]


@pytest.mark.asyncio
async def test_delete_session_not_found(client):
    """DELETE /v1/sessions/{id} con ID inexistente devuelve 404"""
    response = await client.delete("/v1/sessions/nonexistent_session_id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_delete_session_created_success(client):
    """DELETE /v1/sessions/{id} elimina una sesión creada previamente"""
    # Crear una sesión primero mediante un mensaje de chat
    create_payload = {
        "session_id": None,
        "message": "Hola",
        "stream": False,
    }
    create_resp = await client.post("/v1/chat", json=create_payload)
    assert create_resp.status_code == 200

    # Listar sesiones para obtener el ID generado
    list_resp = await client.get("/v1/sessions")
    assert list_resp.status_code == 200
    sessions = list_resp.json().get("sessions", [])
    assert len(sessions) > 0, "Debería haber al menos una sesión tras crear un mensaje"
    session_id = sessions[-1]["id"]

    delete_resp = await client.delete(f"/v1/sessions/{session_id}")
    assert delete_resp.status_code == 204


@pytest.mark.asyncio
async def test_get_sessions(client):
    """GET /v1/sessions devuelve lista de sesiones del usuario"""
    response = await client.get("/v1/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data


@pytest.mark.asyncio
async def test_get_session_not_found(client):
    """GET /v1/sessions/{id} con ID inexistente devuelve 404"""
    response = await client.get("/v1/sessions/nonexistent_session_id")
    assert response.status_code == 404

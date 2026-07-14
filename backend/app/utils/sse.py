from fastapi import Response
from sse_starlette.sse import EventSourceResponse
import json
from typing import AsyncGenerator


def create_sse_response(event_generator: AsyncGenerator):
    """Crea una respuesta SSE"""
    return EventSourceResponse(event_generator)


async def format_sse_event(event_type: str, data: dict) -> str:
    """Formatea un evento SSE"""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
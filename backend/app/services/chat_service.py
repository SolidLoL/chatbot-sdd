from typing import AsyncGenerator
import structlog

logger = structlog.get_logger()


class ChatService:
    """Servicio de chat (mock por ahora, se conectará a Databricks)"""
    
    async def generate_response(
        self,
        session_id: str,
        message: str,
    ) -> dict:
        """Genera una respuesta completa (no streaming)"""
        # TODO: Conectar con Databricks Model Serving
        return {
            "content": f"Respuesta mock para: {message}",
            "citations": [
                {
                    "id": "cite_1",
                    "title": "Documentación de ejemplo",
                    "url": "https://docs.example.com",
                    "snippet": "Este es un snippet de ejemplo",
                    "relevance_score": 0.95,
                }
            ],
            "metadata": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
            }
        }
    
    async def stream_response(
        self,
        session_id: str,
        message: str,
    ) -> AsyncGenerator[dict, None]:
        """Genera una respuesta en streaming"""
        # TODO: Conectar con Databricks Model Serving
        response_text = f"Esta es una respuesta mock para tu pregunta sobre: {message}"
        
        # Simular streaming token por token
        words = response_text.split()
        for i, word in enumerate(words):
            yield {
                "type": "token",
                "data": {"content": word + " "}
            }
        
        # Simular citas
        yield {
            "type": "citation",
            "data": {
                "id": "cite_1",
                "title": "Guía de Databricks",
                "url": "https://docs.databricks.com",
                "snippet": "Documentación oficial de Databricks",
                "relevance_score": 0.92,
            }
        }
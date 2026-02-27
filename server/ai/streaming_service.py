import logging
from typing import Dict, Any
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class DigitalTwinStreamingService:
    """
    Serviço modular para Streaming Interativo do Gêmeo Digital.
    Focado em chamadas de vídeo em tempo real e FAQs vivas.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()
        self.streaming_endpoint = "https://api.heygen.com/v1/streaming.task"

    async def start_interactive_session(self, patient_id: str) -> Dict[str, str]:
        """
        Inicia uma sessão de streaming e retorna os tokens de conexão.
        """
        logger.info(f"🎥 Iniciando Sessão Interativa para o paciente {patient_id}...")
        # MOCK: Chamada para criar session e obter o RTC Server URL
        return {
            "session_id": "STREAM_XYZ_123",
            "rtc_url": "wss://streaming.heygen.com/live",
            "token": "MOCK_SESSION_TOKEN"
        }

    async def process_realtime_input(self, session_id: str, text_input: str):
        """
        Recebe a fala do paciente (via STT) e envia para o Avatar responder.
        """
        # 1. IA decide a resposta no tom do médico
        response_text = await self.llm.generate_text(f"Responda como médico: {text_input}")
        
        # 2. Envia para o motor de streaming falar imediatamente
        logger.info(f"🗣️ Enviando resposta ao Avatar em tempo real: {response_text[:30]}...")
        return response_text

    def log_stream_usage(self, session_id: str, duration_sec: int):
        self.repo.log_bi_event("STREAMING_ACCESSED", {"session": session_id, "duration": duration_sec})

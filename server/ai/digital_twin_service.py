import logging
from typing import Dict, Any
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class DigitalTwinService:
    """
    Serviço modular para Gestão do Gêmeo Digital (Voz e Vídeo).
    Responsável por comunicações ultra-personalizadas.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()
        self.eleven_labs_key = "MOCK_ELEVEN_KEY"
        self.heygen_key = "MOCK_HEYGEN_KEY"

    async def generate_cloned_audio(self, target_text: str, voice_id: str) -> str:
        """
        Gera um áudio usando a voz clonada do médico via ElevenLabs.
        """
        logger.info(f"🎙️ Clonando voz para o texto: {target_text[:30]}...")
        # MOCK: Chamada para https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
        return "server/assets/audio/cloned_response_001.mp3"

    async def create_avatar_video(self, patient_name: str, message: str) -> str:
        """
        Gera um vídeo do avatar do médico falando o nome do paciente via HeyGen.
        """
        logger.info(f"👤 Gerando vídeo customizado para {patient_name}...")
        # MOCK: Chamada para https://api.heygen.com/v1/video.generate
        return "server/assets/video/avatar_welcome_maria.mp4"

    async def talk_as_doctor(self, patient_id: str, context: str):
        """
        IA atua como o médico, gera o texto com o 'tom' dele e depois clona a voz.
        """
        prompt = f"Aja como o Dr. Breno. Use o tom dele para responder sobre {context}. Seja breve e empático."
        doctor_text = await self.llm.generate_text(prompt)
        audio_path = await self.generate_cloned_audio(doctor_text, "BRENO_VOICE_ID")
        return audio_path, doctor_text

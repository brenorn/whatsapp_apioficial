import logging
import os
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

class ElevenLabsEngine:
    """
    Motor Híper-Realista de Áudio (Text-to-Speech via ElevenLabs API).
    Responsável por clonar emoções, respirações e a voz do médico.
    """

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.default_voice_id = os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "pFZP5JQG7iQjIQuC4Bku") # ID genérico
        self.base_url = "https://api.elevenlabs.io/v1"

    async def generate_speech(self, text: str, voice_id: str = None) -> str:
        """
        Recebe um texto e devolve o caminho do arquivo MP3 gerado na pasta assets.
        Retorna None se a API falhar.
        """
        target_voice = voice_id if voice_id else self.default_voice_id
        
        if not self.api_key:
            logger.warning("⚠️ [ELEVENLABS] API Key ausente no .env. Ignorando TTS.")
            return None

        url = f"{self.base_url}/text-to-speech/{target_voice}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2", # Melhor para português BR e emoções
            "voice_settings": {
                "stability": 0.5, # Mantém a flutuação emocional (respiração natural)
                "similarity_boost": 0.75, # Força a IA a ser igualzinha à amostra de voz real
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        logger.info(f"🎙️ [ELEVENLABS] Enviando texto: '{text[:40]}...' para o VoiceLab.")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, headers=headers, timeout=60.0)
                response.raise_for_status()

                # Salvando localmente
                output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "audio"))
                os.makedirs(output_dir, exist_ok=True)
                
                filename = f"twin_audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(response.content)

                logger.info(f"✅ [ELEVENLABS] Áudio gerado e salvo: {filepath}")
                return filepath

            except Exception as e:
                logger.error(f"❌ [ELEVENLABS] Erro na geração de áudio: {str(e)}")
                return None

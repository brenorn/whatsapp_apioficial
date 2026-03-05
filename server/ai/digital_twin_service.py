import logging
import os
from typing import Dict, Any, Tuple
from ai.llm_factory import LLMFactory
from ai.digital_twin.elevenlabs_engine import ElevenLabsEngine

logger = logging.getLogger(__name__)

class DigitalTwinService:
    """
    O Orquestrador do Gêmeo Digital. Responsável pela Clonagem de Voz e Personalidade (Projeto 16).
    Atua integrando o "Cérebro IA" com a "Voz da ElevenLabs".
    """

    def __init__(self):
        self.eleven = ElevenLabsEngine()
        self.audio_dir = "server/assets/audio/"
        
        # Garante a existência do diretório
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir, exist_ok=True)

    async def generate_cloned_audio(self, target_text: str, voice_id: str = None) -> str:
        """
        Dá Play no Text-to-Speech (TTS) com estabilidade emocional calculada pela motor ElevenLabs.
        Retorna o path completo (.mp3) pro WhatsApp enviar via Cloud.
        """
        logger.info(f"👤 [DIGITAL TWIN] Requisitando cordas vocais sintéticas. Texto: '{target_text[:30]}...'")
        audio_path = await self.eleven.generate_speech(target_text, voice_id)
        return audio_path

    async def create_avatar_video(self, patient_name: str, message: str) -> str:
        """
        (P23) HeyGen Avatar Builder - Vídeo com DeepFake positivo.
        Status MOCK (Aguardando Deployer de Tokens).
        """
        logger.warning(f"🎥 (Projeto 23 / HeyGen API em Construção. Vídeo Custom pra: {patient_name}...)")
        return "server/assets/video/avatar_welcome_mock.mp4"

    async def talk_as_doctor(self, patient_id: str, context: str) -> Tuple[str, str]:
        """
        Função VIP 2-EM-1:
        1.  (LLMFactory) Ouve o lead, atua e pensa exatamente como o médico real.
        2.  (ElevenLabsEngine) "Fala" aquilo num áudio ultra-realista que flui como WhatsApp.
        Retorna RotaDoAudio e Texto.
        """
        # A IA entra em 'character' com "system_instruction" pesado
        sys_prompt = "Você é o Doutor, Sênior e especialista da clínica. Escreva EXATAMENTE como se você estivesse enviando um áudio do whatsapp (Sem hashtags, com reticências para respirar e palavras casuais como 'olha, veja bem...'). Fale entre 5 e 12 segundos (Máximo 2 linhas cursivas)."
        
        user_prompt = f"O paciente/cliente ({patient_id}) perguntou ou o contexto é: {context}. Gere o texto do seu áudio de resposta agora."
        
        doctor_text = LLMFactory.generate(prompt=user_prompt, task_level="complex", system_instruction=sys_prompt)
        
        # Joga para a Máquina de Voz Híbrida
        audio_path = await self.generate_cloned_audio(doctor_text)
        
        return audio_path, doctor_text

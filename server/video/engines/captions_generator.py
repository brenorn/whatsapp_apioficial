import logging
import os
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class CaptionsGenerator:
    """
    Gerador de Legendas Magnéticas (Estilo Hormozi).
    Responsável pela transcrição e formatação de texto dinâmico.
    """

    def __init__(self):
        self.output_dir = "server/assets/temp_clips"

    async def generate_magnetic_captions(self, video_path: str) -> str:
        """
        Simula o uso do OpenAI Whisper para transcrição e 
        gera um arquivo .srt ou injeta via FFmpeg.
        """
        logger.info(f"🔡 [CAPTIONS] Gerando legendas magnéticas para {video_path}")
        
        # MOCK DO FLUXO:
        # 1. Extrair Áudio do Vídeo (FFmpeg)
        # 2. Transcrever (Whisper API / Local)
        # 3. Formatar Texto (Quebras curtas, emojis, cores) via IA
        
        # Exemplo de como a IA ajudaria a 'quebrar' as legendas para ficarem viciantes:
        transcription_raw = "Olá hoje vamos falar sobre como escalar sua clínica médica usando IA."
        
        sys_prompt = "Você é um editor de vídeos estilo Alex Hormozi. Quebre a frase abaixo em linhas curtíssimas (max 3 palavras) e adicione 1 emoji pertinente a cada 2 linhas para legendas dinâmicas."
        
        formatted_captions = LLMFactory.generate(
            prompt=transcription_raw,
            task_level="simple",
            system_instruction=sys_prompt
        )
        
        logger.info(f"✨ [AI CAPTIONS]: {formatted_captions}")
        
        # Na versão real, aqui queimaríamos o SRT no vídeo via FFmpeg drawtext
        return video_path

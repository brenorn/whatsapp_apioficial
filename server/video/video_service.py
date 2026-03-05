import logging
import os
from typing import Dict, Any
from video.engines.silence_sniper import SilenceSniper
from video.engines.captions_generator import CaptionsGenerator

logger = logging.getLogger(__name__)

class VideoAutoEditorService:
    """
    Serviço modular para Edição de Vídeo Automatizada.
    Focado em Reels/Social Media de alta conversão.
    """

    def __init__(self):
        self.output_dir = "server/assets/processed_videos/"
        self.temp_dir = "server/assets/temp_clips/"
        self.sniper = SilenceSniper()
        self.captions = CaptionsGenerator()
        
        for d in [self.output_dir, self.temp_dir]:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)

    async def process_video_reels(self, input_path: str, add_subtitles: bool = True) -> str:
        """
        Executa o pipeline completo: Corte de Silêncio -> Legenda -> Branding.
        """
        logger.info(f"🎞️ Iniciando edição automatizada Hormozi-Style: {input_path}")
        
        # 1. Silence Removal (Simulado)
        clean_path = await self._remove_silence(input_path)
        
        # 2. Add Captions via Whisper (Simulado)
        if add_subtitles:
            final_path = await self._add_magnetic_captions(clean_path)
        else:
            final_path = clean_path
            
        return final_path

    async def _remove_silence(self, path: str) -> str:
        """Aciona o motor Silence Sniper para cortes secos e rápidos."""
        output_name = f"snipped_{os.path.basename(path)}"
        out_path = os.path.join(self.temp_dir, output_name)
        return await self.sniper.snip_silence(path, out_path)

    async def _add_magnetic_captions(self, path: str) -> str:
        """Aciona o motor de IA para criar legendas de alta retenção."""
        return await self.captions.generate_magnetic_captions(path)

    def get_download_url(self, video_id: str) -> str:
        """Gera URL de download para o WhatsApp Cloud Client."""
        return f"https://api.clinica.com/videos/download/{video_id}"

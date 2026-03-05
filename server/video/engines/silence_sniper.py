import logging
import os
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)

class SilenceSniper:
    """
    Motor especializado em remoção de silêncio e hesitações (Jump-Cuts).
    Utiliza FFmpeg para detecção de níveis de decibéis e corte cirúrgico.
    """

    def __init__(self, threshold_db: int = -30, duration_sec: float = 0.5):
        self.threshold = threshold_db
        self.min_duration = duration_sec

    async def snip_silence(self, input_path: str, output_path: str) -> str:
        """
        Analisa o vídeo e aplica o filtro 'silencedetect' do FFmpeg.
        Remove gaps onde o áudio está abaixo do threshold.
        """
        if not os.path.exists(input_path):
            logger.error(f"❌ Vídeo não encontrado para Sniper: {input_path}")
            return input_path

        logger.info(f"✂️ [SILENCE SNIPER] Analisando decibéis em {input_path}...")
        
        # Filtro FFmpeg para remover silêncio automaticamente
        # 'silenceremove' é mais direto que detectar e cortar via script externo
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-af', f'silenceremove=stop_periods=-1:stop_duration={self.min_duration}:stop_threshold={self.threshold}dB',
            '-vcodec', 'libx264', '-crf', '23', '-preset', 'veryfast',
            output_path
        ]

        try:
            # Execução via subprocess (FFmpeg deve estar no PATH do Windows)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error(f"❌ [FFMPEG ERROR]: {stderr.decode()}")
                return input_path

            logger.info(f"✅ [SILENCE SNIPER] Silêncio removido com sucesso: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Falha ao executar Silence Sniper: {e}")
            return input_path

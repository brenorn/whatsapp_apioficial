import os
import logging
from ai.llm_factory import LLMFactory
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)

# Requisitamos o CloudClient para download
cloud_client = WhatsAppCloudClient()

class AudioProcessor:
    """
    PROJETO 2: STT Motor (Speech-To-Text) blindado com as normas LGPD / DMAIC.
    Responsabilidade: Pegar um áudio cru via Webhook Meta, usar o Gemini Flash 
    (Multi-modal) para OCR/Transcrever com pontuação médica, e DELETAR os rastros
    (Zero-Retention) do arquivo HD Local.
    """

    @classmethod
    def transcribe_and_cleanup(cls, media_id: str) -> str:
        """
        1. Download API (OGG binario).
        2. Upload Meta/Google (GenAI Files).
        3. OCR Inference com Gemini.
        4. Delete local and Cloud files (Esquecimento LGPD).
        """
        filepath = cloud_client.download_media(media_id)
        
        if not filepath or not os.path.exists(filepath):
            logger.warning(f"⚠️ [STT ENGINE] Áudio {media_id} corrompido ou indisponível na Nuvem da Meta.")
            return "[Error: Áudio Cortado]"
            
        try:
            client = LLMFactory.get_client()
            if not client:
                 return "[IA Sem Visão momentânea de Áudio - Notifique o Dev]"
                 
            logger.info(f"🎙️ [STT ENGINE] Acordando IA Multi-modal Gemini para transcrever: {filepath}")
            
            # API Gemini GenAI Upload
            audio_file = client.files.upload(file=filepath)
            
            # O Prompt Médico-Cirúrgico: Ensina pontuação e gramática (Impede alucinações gagas comuns de áudios).
            prompt = "Transcreva esse áudio do paciente fielmente e de forma profissional. Aplique ortografia correta e pontuações lógicas. Se houver nomes técnicos ou doenças, corrija-os pelo contexto."
            
            # Gemini Flash é a jóia na coroa de Áudio STT (Custa centavos/hora).
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[audio_file, prompt]
            )
            
            transcription = response.text.strip()
            logger.info(f"✅ [STT SUCCESS] Whisper Transcreveu: {transcription[:45]}...")
            
            # Fase LGPD 1 (DELETAR O CACHE DA GOOGLE)
            try:
                client.files.delete(name=audio_file.name)
            except Exception as e_nuvem:
                logger.error(f"⚠️ [LGPD GOOGLE] Arquivo transitorio não explodido no server: {e_nuvem}")
            
            return transcription
            
        except Exception as e:
            logger.error(f"❌ [STT FATAL ALARM] Erro transcrevendo media {media_id}: {str(e)}")
            return "[Não consegui te ouvir bem porque houve uma interferência de sinal. Pode digitar?]"
            
        finally:
            # Fase LGPD 2 (DELETAR DO HD DO SERVIDOR LOCAL DA CLÍNICA)
            try:
                if filepath and os.path.exists(filepath):
                    os.unlink(filepath)
                    logger.info(f"🗑️ [LGPD LOCAL] Binário OGG desmaterializado com sucesso: {filepath}")
            except Exception as e_local:
                logger.warning(f"⚠️ [LGPD LOCAL] Privilégios insuficientes para remover: {e_local}")

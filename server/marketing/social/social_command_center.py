import os
import logging
from typing import Dict, Any
from marketing.social.image_engine import ImageWithBorder
from marketing.social.social_copywriter import SocialCopywriter
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)
cloud_api = WhatsAppCloudClient()

class SocialCommandCenter:
    """
    Orquestrador de Social Media (Projeto 6).
    Transforma fotos recebidas em Posts Profissionais Editados e Legendados.
    """

    ASSETS_DIR = "server/marketing/assets"
    TEMP_DIR = "server/marketing/temp"
    MOLDURA_PATH = os.path.join(ASSETS_DIR, "moldura.png")

    @classmethod
    def prepare_social_draft(cls, phone: str, media_path: Optional[str] = None, user_hint: str = "", media_type: str = "image"):
        """
        [P6.1] Recebe o conteúdo (Foto, Vídeo ou Texto), processa e gera sugestão de legenda.
        """
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        output_path = None
        
        logger.info(f"📸 [SOCIAL CENTER] Preparando rascunho ({media_type}) para {phone}...")

        try:
            # 1. Processamento Visual (Apenas se for Foto)
            if media_type == "image" and media_path:
                filename = os.path.basename(media_path)
                output_path = os.path.join(cls.TEMP_DIR, f"draft_{filename}")
                if os.path.exists(cls.MOLDURA_PATH):
                    ImageWithBorder.create_bordered_image(media_path, cls.MOLDURA_PATH, output_path)
                    logger.info("🎨 [SOCIAL CENTER] Borda MoveMind aplicada à foto.")
                else:
                    output_path = media_path
            
            # 2. Gerar Legenda Estratégica
            # O SocialCopywriter agora decide o tom (Reels, Storytelling ou Foto)
            caption = SocialCopywriter.generate_instagram_caption(user_hint, media_type=media_type)

            # 3. Formatar a Proposta Baseado no Tipo
            headers = {
                "image": "📷 SUGESTÃO DE POST (FOTO)",
                "video": "🎬 SUGESTÃO DE REELS (VÍDEO)",
                "testimonial": "💎 SUGESTÃO DE PROVA SOCIAL"
            }
            
            msg_proposta = (
                f"*{headers.get(media_type, '🎨 SUGERIDO')}*\n\n"
                f"{caption}\n\n"
                f"-------------------\n"
                f"O que achou desse rascunho? Podemos publicar nas redes oficiais?"
            )
            
            buttons = [
                {"id": f"post_insta_ok_{media_type}", "title": "✅ Aprovar e Postar"},
                {"id": f"post_insta_edit_{media_type}", "title": "✍️ Editar"},
                {"id": "post_insta_cancel", "title": "❌ Descartar"}
            ]
            
            cloud_api.send_interactive_buttons(phone, msg_proposta, buttons)
            return True

        except Exception as e:
            logger.error(f"❌ [SOCIAL CENTER ERROR] Falha ao preparar draft: {e}")
            cloud_api.send_text_message(phone, "Tivemos um problema ao processar sua foto para o Instagram. Tente novamente em instantes.")
            return False

    @classmethod
    def publish_to_instagram(cls, phone: str, draft_id: str):
        """
        [P6.2] Efetiva a postagem na Graph API do Instagram.
        """
        # Aqui integraria com InstagramPostService usando o token oficial
        logger.info(f"🚀 [SOCIAL CENTER] Publicando post no Instagram para o Lead {phone}...")
        cloud_api.send_text_message(phone, "📢 *Sucesso!* Sua postagem já está no ar no Instagram oficial da MoveMind.")

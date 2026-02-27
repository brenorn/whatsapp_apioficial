import logging
import requests
from typing import List, Dict
from server.database.repository import Repository

logger = logging.getLogger(__name__)

class OmniPublisherService:
    """
    Serviço Central de Distribuição de Conteúdo Onipresente.
    Lida com as APIs do Facebook/Instagram, TikTok e LinkedIn.
    """

    def __init__(self):
        self.repo = Repository()
        # Em PROD, esses tokens vêm do .env ou DB vault
        self.fb_access_token = "MOCK_FB_TOKEN"
        self.ig_user_id = "MOCK_IG_ID"

    async def publish_to_all(self, media_urls: List[str], caption: str):
        """Dispara a publicação em todas as redes configuradas."""
        results = {}
        results['instagram'] = await self.post_insta_carousel(media_urls, caption)
        results['tiktok'] = await self.post_tiktok_video(media_urls[0], caption)
        results['linkedin'] = await self.post_linkedin_document(media_urls, caption)
        
        # Loga no histórico social
        self.repo.log_social_post(results, caption)
        return results

    async def post_insta_carousel(self, images_urls: List[str], caption: str):
        """Postagem de Carrossel no Instagram (Processo 3 passos)."""
        logger.info("📸 Iniciando postagem de Carrossel no Instagram...")
        # 1. Criar Containers (MOCK)
        item_ids = []
        # Para cada URL, faria um POST /media?image_url=URL...
        
        # 2. Criar Container Pai (Carousel)
        # res = requests.post(f"https://graph.facebook.com/v21.0/{self.ig_user_id}/media", ...)
        
        # 3. Publicar
        return {"status": "success", "platform": "instagram", "id": "IG12345"}

    async def post_tiktok_video(self, video_url: str, caption: str):
        """Postagem de Vídeo no TikTok via Content Posting API."""
        logger.info("🎥 Iniciando postagem no TikTok...")
        return {"status": "success", "platform": "tiktok", "id": "TK67890"}

    async def post_linkedin_document(self, images_urls: List[str], caption: str):
        """Postagem de Carrossel (PDF Document) no LinkedIn."""
        logger.info("💼 Iniciando postagem de documento no LinkedIn...")
        return {"status": "success", "platform": "linkedin", "id": "LI_DOC_001"}

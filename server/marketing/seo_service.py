import logging
import json
from typing import Dict, Any
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class SEOService:
    """
    Serviço modular para Criação de Conteúdo SEO com Autoridade Médica.
    Focado em E-E-A-T e Schema.org.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()
        self.wp_url = "https://seublog.com.br/wp-json/wp/v2/posts"

    async def generate_medical_article(self, raw_content: str) -> Dict[str, str]:
        """
        Transforma áudio/texto bruto em um artigo científico-popular de alta conversão.
        """
        logger.info("✍️ Gerando artigo SEO com E-E-A-T...")
        
        prompt = f"""
        Aja como um Redator Médico Especialista em SEO (E-E-A-T).
        Transforme este conteúdo bruto em um artigo para blog:
        "{raw_content}"
        
        Requisitos:
        1. Título H1 magnético.
        2. Subtítulos H2 e H3 com palavras-chave de cauda longa.
        3. Linguagem técnica mas acessível (Autoridade Médica).
        4. Sugestão de Meta Description.
        5. Gere o código JSON-LD de Schema.org (MedicalWebPage).
        """
        
        article_data = await self.llm.generate_structured(prompt)
        return article_data

    async def publish_to_wordpress(self, title: str, content: str, status: str = "draft"):
        """
        Envia o artigo gerado diretamente para o blog da clínica.
        """
        logger.info(f"🌐 Publicando rascunho '{title}' no WordPress...")
        # MOCK: Chamada requests.post aqui com Auth Header
        return {"status": "success", "url": f"https://blog.clinica.com/{title.lower().replace(' ', '-')}"}

    def generate_schema_ld(self, title: str, author: str):
        """Cria o objeto JSON-LD para SEO avançado."""
        schema = {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "headline": title,
            "author": {"@type": "Person", "name": author},
            "specialty": "Medical Aesthetics"
        }
        return json.dumps(schema)

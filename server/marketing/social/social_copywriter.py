import logging
from typing import Optional
from ai.llm_factory import LLMFactory
from ai.knowledge_manager import KnowledgeManager

logger = logging.getLogger(__name__)

class SocialCopywriter:
    """
    Substituto LEVE e RÁPIDO para o CrewAI.
    Usa o LLMFactory (Gemini 2.5 Pro) para gerar legendas de alta conversão
    baseadas na identidade visual e no conhecimento do RAG.
    """

    @classmethod
    def generate_instagram_caption(cls, user_hint: str, image_description: Optional[str] = None, media_type: str = "image") -> str:
        """
        Gera uma legenda profissional adaptada ao tipo de mídia (Foto, Vídeo ou Depoimento).
        """
        context = KnowledgeManager.get_full_context()
        
        # Ajuste dinâmico de tom baseado no formato
        format_instructions = {
            "image": "Foque em estética, diferenciais e uma CTA direta.",
            "video": "Crie um HOOK (Gancho) matador nos primeiros 2 segundos. Use bullet points para facilitar a leitura rápida. Estilo Reels.",
            "testimonial": "Destaque a PROVA SOCIAL. Transforme a dica do usuário em uma história de superação ou sucesso (Storytelling)."
        }.get(media_type, "Foque em engajamento.")

        prompt = f"""
        Você é um Diretor de Criação e Estrategista de Conteúdo Senior para a clínica MoveMind.
        
        TIPO DE MÍDIA: {media_type.upper()}
        INSTRUÇÃO DE FORMATO: {format_instructions}

        CONTEXTO DA CLÍNICA (RAG):
        {context}

        DICA DO USUÁRIO / TRANSCRIÇÃO:
        {user_hint}

        DESCRIÇÃO VISUAL (SE HOUVER):
        {image_description or "Conteúdo Institucional"}

        REGRAS DE OURO:
        1. Tom: Inspirador, profissional e humano.
        2. Gatilhos: Autoridade, Lógica e Prova Social.
        3. CTA: Direcione para o WhatsApp ou Link na Bio.
        4. Hashtags: 5 a 10 estratégicas.
        
        FORMATO DE SAÍDA:
        Apenas o texto da legenda pronto para postar.
        """

        logger.info(f"✍️ [SOCIAL COPY] Refinando copy para {media_type} via Gemini Pro...")
        
        try:
            return LLMFactory.generate(prompt, task_level="complex")
        except Exception as e:
            logger.error(f"❌ [SOCIAL COPY ERROR] {e}")
            return f"🌟 Transformação MoveMind: {user_hint}"

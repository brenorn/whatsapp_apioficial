import logging
from ai.llm_factory import LLMFactory
from ai.knowledge_manager import KnowledgeManager

logger = logging.getLogger(__name__)

class ContentTransformer:
    """
    Transformador de Conteúdo Denso (Projeto 7).
    Pega artigos, textos longos ou áudios e 'mastiga' em rascunhos de rede social.
    """

    @classmethod
    def transform_long_content(cls, raw_content: str, target_format: str = "instagram_post") -> str:
        """
        Pega um conteúdo bruto (Artigo, Transcrição de Áudio) e transforma em posts.
        """
        clinic_context = KnowledgeManager.get_full_context()

        prompt = f"""
        Você é um Redator de Performance. Sua missão é fazer "Content Repurposing".
        Transforme o conteúdo bruto abaixo em um post de {target_format} focado na Clínica MoveMind.

        CONTEÚDO BRUTO (Artigo/Áudio/Texto):
        {raw_content}

        CONTEXTO DA CLÍNICA:
        {clinic_context}

        REGRAS:
        1. Extraia os 3 pontos mais importantes (Sumarização seletiva).
        2. Linguagem adaptada para o Instagram (Visual, curta, direta).
        3. Mantenha o tom profissional mas acessível.
        4. Crie um Hook (Gancho) chamativo baseado no texto.

        FORMATO DE SAÍDA:
        Um post completo com legenda, emojis e hashtags.
        """

        logger.info(f"🔄 [CONTENT TRANSFORMER] Transformando conteúdo longo em {target_format}...")

        try:
            return LLMFactory.generate(prompt, task_level="complex")
        except Exception as e:
            logger.error(f"❌ [TRANSFORMER ERROR] {e}")
            return f"Resumo do seu conteúdo: {raw_content[:100]}..."

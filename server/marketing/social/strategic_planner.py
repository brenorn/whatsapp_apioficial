import logging
from typing import List, Dict
from ai.llm_factory import LLMFactory
from ai.knowledge_manager import KnowledgeManager

logger = logging.getLogger(__name__)

class StrategicPlanner:
    """
    Motor de Planejamento Estratégico (Projeto 7).
    Transforma ideias soltas ou artigos em calendários editoriais completos.
    """

    @classmethod
    def generate_weekly_plan(cls, user_input: str) -> str:
        """
        Gera um plano de 7 dias baseado no contexto da clínica e no input do usuário.
        """
        clinic_context = KnowledgeManager.get_full_context()
        
        prompt = f"""
        Você é o CMO (Chief Marketing Officer) da MoveMind especializado em Growth Hacking.
        Sua tarefa é criar um CRONOGRAMA SEMANAL (7 dias) de postagens para o Instagram.

        CONTEÚDO BASE / DICA DO USUÁRIO:
        {user_input}

        CONTEXTO DA CLÍNICA (SERVIÇOS E REGRAS):
        {clinic_context}

        REQUISITOS DO PLANO:
        1. 7 Dias: Segunda a Domingo.
        2. Mix de Formatos: Alternar entre Reels (Vídeo), Carrossel (Informativo) e Foto (Lifestyle/Autoridade).
        3. Funil de Conteúdo: 
           - Topo (Atração): Dicas gerais.
           - Meio (Autoridade): Resultados e Metodologia MoveMind.
           - Fundo (Venda): CTA direta para agendamento.
        4. Ganchos: Sugira um título impactante para cada dia.

        SAÍDA:
        Formate como um calendário de fácil leitura no WhatsApp, com emojis e tópicos claros.
        """

        logger.info("📅 [STRATEGIC PLANNER] Gerando Calendário Editorial Semanal...")
        
        try:
            return LLMFactory.generate(prompt, task_level="complex")
        except Exception as e:
            logger.error(f"❌ [PLANNER ERROR] {e}")
            return "Não consegui gerar o plano agora. Mas tente postar algo sobre seus resultados hoje!"

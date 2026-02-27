import logging
from typing import Dict, Any, List
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class MeetingIntelService:
    """
    Serviço modular para Extração de Inteligência de Reuniões e Consultas.
    Gera Atas, Action Items e Mapas Mentais.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()

    async def process_consultation_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Analisa uma transcrição e extrai os pontos chave.
        """
        logger.info("🧠 Extraindo inteligência da consulta...")
        
        prompt = f"""
        Analise a seguinte transcrição de consulta/reunião:
        "{transcript}"
        
        Extraia:
        1. Resumo Executivo (Bullet points).
        2. Action Items (Quem faz o que e quando).
        3. Código Mermaid.js para um Mapa Mental da discussão.
        
        Retorne em JSON estruturado.
        """
        
        intel = await self.llm.generate_structured(prompt)
        return intel

    async def generate_mermaid_flow(self, process_description: str) -> str:
        """
        Gera o código Mermaid para visualização de fluxos.
        """
        prompt = f"Gere apenas o código Mermaid.js (graph TD) para: {process_description}"
        mermaid_code = await self.llm.generate_text(prompt)
        return mermaid_code

    def save_insights(self, phone: str, intel_data: Dict):
        """Salva os insights no banco para consulta futura no Projeto 8."""
        self.repo.log_meeting_insight(phone, intel_data)

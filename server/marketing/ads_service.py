import logging
from typing import Dict, Any
from database.repository import Repository
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class GoogleAdsService:
    """
    Serviço modular para Gestão de Google Ads.
    Permite controle de campanhas e orçamentos via WhatsApp.
    """

    def __init__(self):
        self.repo = Repository()
        self.developer_token = "MOCK_DEV_TOKEN"
        self.client_id = "MOCK_CLIENT_ID"

    async def get_performance_summary(self, customer_id: str) -> Dict[str, Any]:
        """
        Gera um resumo de performance (Gasto, Impressões, Cliques, Conversões).
        """
        logger.info(f"📊 Buscando performance Ads para {customer_id}...")
        # MOCK: Aqui entraria a chamada de query GAQL
        summary = {
            "spend": 150.50,
            "clicks": 450,
            "conversions": 12,
            "cpc": 0.33,
            "cpa": 12.54
        }
        return summary

    async def adjust_budget(self, campaign_id: str, new_budget: float):
        """
        Altera o orçamento diário de uma campanha.
        """
        logger.warning(f"💰 Ajustando orçamento da campanha {campaign_id} para R$ {new_budget}")
        # Lógica de Update via API aqui
        return f"✅ Orçamento da campanha {campaign_id} atualizado para R$ {new_budget}."

    async def analyze_and_suggest(self, customer_id: str):
        """
        IA analisa os dados e sugere ações táticas ao gestor.
        """
        perf = await self.get_performance_summary(customer_id)
        prompt = f"""
        Dados de Tráfego de Ontem: {perf}
        Aja como um gestor de tráfego sênior. 
        O desempenho está bom? O que você recomendaria fazer com o orçamento?
        Responda em 3 bullet points curtos para WhatsApp.
        """
        suggestion = LLMFactory.generate(prompt, task_level="complex")
        return suggestion

import logging
from typing import Dict, Any
from database.repository import Repository
from ai.llm_factory import LLMFactory
from commerce.tactical_negotiator import TacticalNegotiator

logger = logging.getLogger(__name__)

class NegotiationService:
    """
    Serviço modular para Negociação de Vendas de Alto Impacto.
    Utiliza técnicas do FBI (Chris Voss) e Matriz de LTV.
    """

    def __init__(self):
        self.repo = Repository()

    async def negotiate(self, phone: str, objection: str, product_value: float) -> str:
        """
        Entra em modo de negociação tática baseado na objeção do cliente.
        """
        from core.experiment_service import ExperimentService
        
        logger.info(f"🤝 Iniciando negociação com {phone} para valor R$ {product_value}")
        
        # 1. Busca LTV do Paciente para definir margem
        ltv_rank = self._calculate_ltv_rank(phone)
        max_discount = 0.05 if ltv_rank == "New" else 0.15
        
        # 2. Negociação Tática (Chris Voss) vs Fallback
        product_ctx = f"Serviço de R$ {product_value}"
        response = await TacticalNegotiator.handle_objection(objection, product_ctx)
        
        return response

    def _calculate_ltv_rank(self, phone: str) -> str:
        # MOCK: Lógica que bateria no DB para ver faturamento acumulado
        return "VIP" # Exemplo

    def save_negotiation_log(self, phone: str, original_val: float, final_val: float, status: str):
        self.repo.log_negotiation(phone, original_val, final_val, status)

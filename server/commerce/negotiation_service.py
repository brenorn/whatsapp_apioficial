import logging
from typing import Dict, Any
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class NegotiationService:
    """
    Serviço modular para Negociação de Vendas de Alto Impacto.
    Utiliza técnicas do FBI (Chris Voss) e Matriz de LTV.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()

    async def negotiate(self, phone: str, objection: str, product_value: float) -> str:
        """
        Entra em modo de negociação tática baseado na objeção do cliente.
        """
        from core.experiment_service import ExperimentService
        
        logger.info(f"🤝 Iniciando negociação com {phone} para valor R$ {product_value}")
        
        # 1. Busca LTV do Paciente para definir margem
        ltv_rank = self._calculate_ltv_rank(phone)
        max_discount = 0.05 if ltv_rank == "New" else 0.15
        
        # 2. Teste A/B de Prompt (Chris Voss vs Jordan Belfort/Direto)
        version = ExperimentService.get_version(phone, "sales_negotiation_v1")
        
        prompt_a = "Aja como um Negociador de Elite (Chris Voss). Use Empatia Tática e Rotulagem."
        prompt_b = "Aja como um Vendedor Direto e Persuasivo (Jordan Belfort). Foque em escassez e fechamento rápido."
        
        selected_persona = ExperimentService.get_prompt_variant(prompt_a, prompt_b, version)
        
        prompt = f"""
        {selected_persona}
        Objeção: "{objection}"
        Valor do Produto: {product_value}
        Margem Máxima Permitida: {max_discount * 100}%
        """
        
        response = await self.llm.generate_text(prompt)
        return response

    def _calculate_ltv_rank(self, phone: str) -> str:
        # MOCK: Lógica que bateria no DB para ver faturamento acumulado
        return "VIP" # Exemplo

    def save_negotiation_log(self, phone: str, original_val: float, final_val: float, status: str):
        self.repo.log_negotiation(phone, original_val, final_val, status)

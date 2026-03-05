import logging
import json
from typing import Dict, Any, Optional
from core.guardrails.vazamento_avancado import PIIValidator
from core.guardrails.ban_list_validator import BanListValidator

logger = logging.getLogger(__name__)

class GuardrailsManager:
    """
    Controlador Central de Guardrails (Escudo de Dados).
    Focado em Economia de Tokens, Segurança e Lógica Determinística.
    """

    @staticmethod
    def validate_input(text: str) -> Dict[str, Any]:
        """
        Valida a entrada do usuário antes de chegar na IA.
        """
        # 1. Ban List (Toxicidade)
        if not BanListValidator.validate(text):
            return {"status": "BLOCKED", "reason": "Toxicidade detectada."}

        # 2. Topic Check (Lógica Pura)
        text_upper = text.upper()
        if "PIX" in text_upper or "PAGAMENTO" in text_upper:
            return {"status": "DETERMINISTIC", "route": "PAYMENT"}

        return {"status": "PASSED"}

    @staticmethod
    def validate_output(ai_response: str, context: str) -> str:
        """
        Higieniza a saída da IA antes de enviar ao WhatsApp.
        """
        # 1. Filtro de PII (Proteção LGPD)
        clean_text = PIIValidator.anonymize(ai_response)
        
        # 2. Filtro de Palavras Proibidas (Censura de saída)
        clean_text = BanListValidator.censor(clean_text)
        
        return clean_text

    @staticmethod
    def check_hallucination(response: str, facts: str) -> bool:
        """
        Validação RAG (Projeto 22). Somente para dados críticos.
        """
        # Aqui chamaria o LlmRagEvaluator do diretório guardrails
        return True

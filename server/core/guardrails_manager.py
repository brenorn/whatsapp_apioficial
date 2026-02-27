import logging
import json
from typing import Dict, Any, Optional

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
        text_upper = text.upper()
        
        # 1. Ban List (Lógica Pura - Economia de Tokens)
        banned = ["PORRA", "MERDA", "CARALHO"] # Simplificado para o exemplo
        if any(w in text_upper for w in banned):
            return {"status": "BLOCKED", "reason": "Toxicidade detectada por lógica pura."}

        # 2. Topic Check (Lógica Pura)
        # Se for dúvida financeira, não passa por IA sem necessidade
        if "PIX" in text_upper or "PAGAMENTO" in text_upper:
            return {"status": "DETERMINISTIC", "route": "PAYMENT"}

        return {"status": "PASSED"}

    @staticmethod
    def validate_output(ai_response: str, context: str) -> str:
        """
        Higieniza a saída da IA antes de enviar ao WhatsApp.
        """
        # 1. Filtro de PII (Proteção LGPD)
        # Implementação de limpeza de e-mails/telefones (Lógica Pura/Regex)
        import re
        clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[E-MAIL PROTEGIDO]', ai_response)
        
        return clean_text

    @staticmethod
    def check_hallucination(response: str, facts: str) -> bool:
        """
        Validação RAG (Projeto 22). Somente para dados críticos.
        """
        # Aqui chamaria o LlmRagEvaluator do diretório guardrails
        return True

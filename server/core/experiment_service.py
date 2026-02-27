import logging
import hashlib
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExperimentService:
    """
    Serviço modular para Gestão de Testes A/B em Fluxos de IA.
    Permite testar prompts, tons de voz e fluxos de agendamento.
    """

    @staticmethod
    def get_version(phone: str, experiment_name: str) -> str:
        """
        Determina qual versão (A ou B) o usuário deve ver. 
        Utiliza um hash determinístico para manter a consistência (Sticky).
        """
        hash_val = int(hashlib.md5(f"{phone}:{experiment_name}".encode()).hexdigest(), 16)
        version = "B" if hash_val % 2 == 1 else "A"
        
        logger.info(f"🧪 [EXPERIMENT] Usuário {phone} alocado na Versão {version} do teste '{experiment_name}'")
        return version

    @staticmethod
    def get_prompt_variant(variant_a: str, variant_b: str, version: str) -> str:
        """Retorna o prompt baseado na variante sorteada."""
        return variant_a if version == "A" else variant_b

import logging
import re
from typing import Dict, Any
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class GroupIntelService:
    """
    Serviço modular para Gestão de Comunidades e Grupos de WhatsApp.
    Atua como moderador e minerador de leads.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()
        self.banned_terms = ["concorrente", "link proibido", "ofensa", "palavrão"] # Exemplo MOCK

    async def moderate_message(self, group_id: str, phone: str, message: str) -> bool:
        """
        Verifica se a mensagem viola alguma regra do grupo.
        Retorna True se estiver tudo OK, False se for violada.
        """
        # 1. Filtro Simples (Anti-Spam / Links)
        if "http" in message.lower() and phone not in self._get_admins():
            logger.warning(f"🚫 [SPAM] Link detectado no grupo {group_id} por {phone}")
            return False
            
        # 2. IA analisa toxicidade ou intenção comercial externa
        if any(term in message.lower() for term in self.banned_terms):
            return False

        return True

    async def scout_leads(self, group_id: str, phone: str, message: str):
        """
        Usa IA para identificar se o membro está pedindo preços ou demonstrando interesse.
        """
        prompt = f"""
        Identifique a intenção desta mensagem em um grupo de estética:
        "{message}"
        
        A pessoa quer comprar algo ou agendar agora? (Sim/Não). 
        Retorne apenas Sim ou Não.
        """
        is_hot_lead = await self.llm.generate_text(prompt)
        
        if "Sim" in is_hot_lead:
            logger.info(f"🔥 [HOT LEAD] Membro {phone} demonstrou interesse no grupo {group_id}!")
            self.repo.log_hot_lead(phone, group_id, message)

    def _get_admins(self):
        # MOCK: Implementar busca em tabela de permissões
        return ["5511999999999"]

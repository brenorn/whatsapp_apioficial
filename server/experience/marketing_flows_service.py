import logging
import json
from typing import Dict, Any
from server.database.repository import Repository

logger = logging.getLogger(__name__)

class MarketingFlowsService:
    """
    Serviço modular para Gestão do Mini-App de Marketing (WhatsApp Flows).
    Permite aprovações e controle de KPIs via interface nativa Meta.
    """

    def __init__(self):
        self.repo = Repository()

    async def trigger_marketing_dashboard(self, admin_phone: str):
        """
        Envia o Flow Interativo (Dashboard) para o Admin.
        """
        logger.info(f"📲 Enviando Dashboard de Marketing (Flow) para {admin_phone}...")
        
        # MOCK de dados para o Flow
        screen_data = {
            "campaigns_active": 3,
            "leads_today": 14,
            "pending_approvals": 2
        }
        
        # Chama o Cloud Client para disparar o Flow
        from core.whatsapp_cloud_client import WhatsAppCloudClient
        cloud_api = WhatsAppCloudClient()
        
        # O flow_id deve ser criado no painel da Meta
        cloud_api.send_flow_message(
            admin_phone, 
            "📊 *MARKETING COMMAND CENTER*\nToque abaixo para gerenciar sua clínica:",
            flow_id="MARKETING_DASH_001",
            screen_id="SCREEN_MAIN",
            initial_data=screen_data
        )

    async def handle_flow_response(self, phone: str, response_json: str):
        """
        Processa o clique/dados vindo do Mini-App (Flow).
        """
        data = json.loads(response_json)
        action = data.get("action")
        
        if action == "approve_post":
            logger.info(f"✅ Post Aprovado via Flow por {phone}!")
            # Acionaria o Projeto 12 (Omnipublisher)
            return "Post aprovado e agendado para todas as redes!"
            
        return "Ação registrada com sucesso."

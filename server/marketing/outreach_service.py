import logging
from typing import Dict, Any, List
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class OutreachService:
    """
    Serviço modular para Prospecção Conversacional Ativa.
    Identifica oportunidades no histórico e inicia conversas de venda.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()

    async def scan_and_trigger_outreach(self, limit: int = 10):
        """
        Varre o banco em busca de pacientes que não aparecem há 6 meses.
        """
        logger.info("🔍 Iniciando Escaneamento de Prospecção Ativa (RFM)...")
        # MOCK: Lista de pacientes 'esquecidos'
        hot_list = [
            {"phone": "5511988887777", "name": "Maria", "last_procedure": "Botox", "days_ago": 185}
        ]
        
        for patient in hot_list:
            await self._send_personalized_offer(patient)

    async def _send_personalized_offer(self, patient: Dict):
        """
        Gera um script humano e envia a oferta.
        """
        prompt = f"""
        Paciente: {patient['name']}
        Último Procedimento: {patient['last_procedure']} há {patient['days_ago']} dias.
        Aja como o Dr. Breno. Mande um 'Oi' sincero, pergunte como ela está e mencione que o efeito do {patient['last_procedure']} deve estar acabando. 
        Não seja vendedor chato. Seja um médico atencioso.
        """
        script = await self.llm.generate_text(prompt)
        
        # Opcional: Usaria o Módulo 16 (Digital Twin) para enviar um ÁUDIO clonado aqui!
        from core.whatsapp_cloud_client import WhatsAppCloudClient
        cloud_api = WhatsAppCloudClient()
        cloud_api.send_text_message(patient['phone'], script)
        
        self.repo.log_outreach(patient['phone'], "REENGAGEMENT_BOTOX")
        logger.info(f"🚀 Outreach enviado para {patient['phone']}")

    def log_outreach_result(self, phone: str, action: str):
        self.repo.log_outreach(phone, action)

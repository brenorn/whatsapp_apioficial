import logging
from typing import Dict, Any
from database.repository import Repository
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class NPSService:
    """
    Serviço modular para NPS 3.0 e Jornada de Encantamento.
    """

    def __init__(self):
        self.repo = Repository()

    async def send_nps_invite(self, phone: str, service_name: str):
        """
        Envia o convite de NPS após um atendimento concluído.
        """
        message = f"Olá! Gostaríamos de saber: de 0 a 10, o quanto você recomendaria o serviço de *{service_name}* da nossa clínica para um amigo?"
        # Chama a API do WhatsApp (Mock ou Real)
        from core.whatsapp_cloud_client import WhatsAppCloudClient
        cloud_api = WhatsAppCloudClient()
        cloud_api.send_text_message(phone, message)
        
        logger.info(f"NPS Invite enviado para {phone}")

    async def process_nps_score(self, phone: str, score: int, feedback: str = ""):
        """
        Processa a nota e define a jornada (Detrator, Neutro, Promotor).
        """
        # 1. Salva no banco
        self.repo.save_nps_response(phone, score, feedback)
        
        # 2. Lógica de Segmentação
        if score <= 6:
            return await self._handle_detractor(phone, feedback)
        elif score >= 9:
            return await self._handle_promoter(phone)
        else:
            return "Obrigado pelo seu feedback! Ele é muito importante para nós."

    async def _handle_detractor(self, phone: str, feedback: str):
        """Recuperação de Detrator: Alerta imediato e pedido de desculpas sincero."""
        logger.warning(f"🚨 DETRATOR DETECTADO: {phone} deu nota baixa.")
        return "Sentimos muito por não termos superado suas expectativas. Um de nossos gestores entrará em contato pessoalmente para entender como podemos melhorar."

    async def _handle_promoter(self, phone: str):
        """Jornada de Promotor: Member-gets-Member (Referral)."""
        coupon = f"AMIGO-{phone[-4:]}"
        return f"Uau! Ficamos muito felizes! 🎉 Como você é um cliente especial, que tal presentear um amigo com 10% de desconto? Use o cupom *{coupon}*."

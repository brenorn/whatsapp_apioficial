import logging
import asyncio
from typing import List, Dict
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)
cloud_api = WhatsAppCloudClient()

class BroadcastEngine:
    """
    Motor de Disparo em Massa (Broadcast Engine).
    Implementa envio assíncrono para bases frias usando templates oficiais.
    """

    @classmethod
    async def send_mass_broadcast(cls, leads: List[Dict[str, str]], template_name: str) -> Dict[str, int]:
        """
        [P5.1] Dispara mensagens para uma lista de leads.
        """
        success_count = 0
        fail_count = 0
        
        logger.info(f"🚀 [BROADCAST] Iniciando disparo para {len(leads)} leads...")

        for lead in leads:
            phone = lead.get("phone")
            try:
                # Meta Rate Limit: Tier 1 suporta 80 mensagens por segundo.
                # Para segurança BMAD, colocamos um pequeno delay entre disparos.
                success = cloud_api.send_template_message(phone, template_name)
                
                if success:
                    success_count += 1
                else:
                    fail_count += 1
                
                await asyncio.sleep(0.1) # 100ms de respiro entre mensagens
                
            except Exception as e:
                logger.error(f"❌ [BROADCAST] Erro no lead {phone}: {e}")
                fail_count += 1

        logger.info(f"🏁 [BROADCAST] Finalizado. Sucessos: {success_count}, Falhas: {fail_count}")
        return {"success": success_count, "failed": fail_count}

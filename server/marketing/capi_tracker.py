import os
import hashlib
import requests
import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CAPITracker:
    """
    Módulo de Marketing (Marketing Hub).
    Implementa a Conversions API (CAPI) da Meta para atribuição de vendas.
    Garante que o Facebook saiba exatamente quem converteu via WhatsApp.
    """
    
    API_VERSION = "v21.0"
    PIXEL_ID = os.getenv("META_PIXEL_ID", "1234567890_pixel")
    ACCESS_TOKEN = os.getenv("META_API_TOKEN") # O mesmo do WhatsApp
    
    @classmethod
    def _hash_data(cls, data: str) -> str:
        """Aplica SHA-256 exigido pela Meta para LGPD/Privacidade."""
        if not data:
            return ""
        return hashlib.sha256(data.strip().lower().encode('utf-8')).hexdigest()

    @classmethod
    def track_purchase(cls, phone: str, value: float, currency: str = "BRL", order_id: str = None) -> bool:
        """
        [P4.1] Envia evento de 'Purchase' para o Pixel da Meta.
        Invocado pelo OrderProcessor assim que o PIX é gerado/pago.
        """
        if not cls.ACCESS_TOKEN or not cls.PIXEL_ID:
            logger.warning("⚠️ [CAPI TRACKER] PIXEL_ID ou TOKEN ausentes. Evento ignorado.")
            return False

        logger.info(f"📊 [CAPI TRACKER] Reportando venda de {currency} {value} para o Lead {phone}.")

        url = f"https://graph.facebook.com/{cls.API_VERSION}/{cls.PIXEL_ID}/events"
        
        # Anonimização hashada (Normas de Segurança Meta/LGPD)
        hashed_phone = cls._hash_data(phone)
        
        event_data = {
            "data": [
                {
                    "event_name": "Purchase",
                    "event_time": int(time.time()),
                    "action_source": "chat",
                    "event_id": order_id or f"ORDER_{int(time.time())}",
                    "user_data": {
                        "ph": [hashed_phone], # Telefone hasheado
                        # No futuro aqui capturamos o fbc (click id) e fbp (browser id)
                    },
                    "custom_data": {
                        "value": value,
                        "currency": currency.upper()
                    }
                }
            ]
        }

        try:
            resp = requests.post(url, params={"access_token": cls.ACCESS_TOKEN}, json=event_data, timeout=10)
            if resp.status_code == 200:
                logger.info(f"✅ [CAPI TRACKER] Evento Purchase enviado com sucesso (PIXEL: {cls.PIXEL_ID})")
                return True
            else:
                logger.error(f"❌ [CAPI TRACKER] Falha na Meta API: {resp.text}")
                return False
        except Exception as e:
            logger.error(f"❌ [CAPI TRACKER] Erro de rede ao reportar CAPI: {e}")
            return False

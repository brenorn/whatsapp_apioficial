import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MetaAdsEngine:
    """
    Conector MOCK para Meta Ads (Facebook & Instagram).
    Pendência: pip install facebook_business
    """

    def __init__(self):
        # MOCK: Será substituído via os.environ.get('META_ADS_TOKEN')
        self.access_token = "MOCK_META_TOKEN"
        self.ad_account_id = "act_123456789"

    async def get_yesterday_performance(self) -> Dict[str, Any]:
        """Extrai o gasto (Spend), CTR (Cliques/Impressões) e CPL."""
        logger.info("🔵 [META ADS] Extraindo relatórios do Gerenciador de Negócios...")
        
        # MOCK RETURN: O JSON que a API da Meta retornaria (Insights)
        return {
            "platform": "Meta (Insta/Face)",
            "spend_brl": 450.00,
            "impressions": 15000,
            "clicks": 320,
            "ctr_percent": 2.1,
            "leads": 8,
            "cpl_brl": 56.25,
            "top_campaign": "Conversão - Reels Terapia"
        }

    async def pause_underperforming_ads(self, cpl_limit: float = 100.0) -> str:
        """Pausa automaticamente campanhas que estão queimando dinheiro cru."""
        logger.warning(f"🛑 [META ADS] Pausando Ads que passaram do CPL BRL {cpl_limit}")
        return "2 Anúncios ruins pausados com sucesso."

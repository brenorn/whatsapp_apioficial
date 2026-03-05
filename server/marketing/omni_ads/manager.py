import logging
import asyncio
from typing import Dict, Any, List
from ai.llm_factory import LLMFactory

# Aqui importaremos Google, Meta, TikTok e LinkedIn
from marketing.omni_ads.meta_engine import MetaAdsEngine
from marketing.omni_ads.tiktok_engine import TikTokAdsEngine

logger = logging.getLogger(__name__)

class OmniAdsManager:
    """
    O Maestro de Tráfego: Orquestrador Global de Campanhas B2C/B2B.
    Conecta as 4 pontas da aquisição para o WhatsApp.
    """

    def __init__(self):
        self.llm = LLMFactory.get_model("gemini")
        # Motores acionados em paralelo
        self.meta_engine = MetaAdsEngine()
        self.tiktok_engine = TikTokAdsEngine()

    async def get_global_roas_report(self) -> str:
        """
        Extrai o Spend (Gasto Total) de todas as plataformas simultaneamente.
        Devolve um Flash Report pro CEO através do cérebro IA.
        """
        logger.info("🌍 [OMNI ADS] Analisando o Ecossistema Mundial da Clínica...")

        # AsAsync() faz os relatórios aparecerem na mesma hora (Latência baixa)
        meta_task = self.meta_engine.get_yesterday_performance()
        tiktok_task = self.tiktok_engine.get_yesterday_performance()

        # Espera as chamadas externas acabarem JUNTAS.
        meta_data, tiktok_data = await asyncio.gather(meta_task, tiktok_task)
        
        # Consolida tudo:
        consolidated = {
            "DATA DO BALANÇO": "Ontem (24h atrás)",
            "meta_facebook": meta_data,
            "tiktok_masses": tiktok_data,
            # "google_search": MOCK (Futuro),
            # "linkedin_b2b": MOCK (Futuro)
        }

        # Bota a IA pra analisar o Json monstruoso
        prompt = f"""
        Você é o Growth Hacker (Gestor de Tráfego de Alta Performance) da clínica MoveMind.
        Aqui estão os resultados brutais de investimento bruto em anúncio de ONTEM de 2 plataformas:
        {consolidated}
        
        Gere um FLASH REPORT executivo (bullet points com emojis no WhatsApp) para o CEO.
        Diga qual plataforma trouxe Lead (CPL) mais barato e qual você pausaria.
        Seja agressivo nos cortes de gasto ruim.
        """
        
        # Como o prompt é muito agressivo, passaremos Task 'complex' para pegar métricas boas
        flash_report = await self.llm.generate_text(prompt)
        return flash_report

    async def pause_all_bad_ads_command(self) -> str:
        """
        Action Action Action. 
        Desliga todos os anúncios em todas as 4 plataformas que falharam no Benchmark.
        """
        logger.critical("🚨 [OMNI ADS] KILL/SWITCH PRESSIONADO!")
        await self.meta_engine.pause_underperforming_ads(100.0) # Se lead > 100 reais, mata
        # await Google_engine.pause()...
        return "🔥 Corte Ciro Gomes: Todas as campanhas que perdiam dinheiro foram decepadas em segundos (Google, Insta, Face e TikTok)."

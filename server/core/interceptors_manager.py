import logging
import os
from database.repository import Repository

logger = logging.getLogger(__name__)

class InterceptorsManager:
    """
    Gerenciador de Interceptadores de Projetos (P9-P25).
    Desafoga o Orquestrador Central.
    """

    @staticmethod
    async def process_intent(phone: str, message: str, intent_data: dict, cloud_api):
        intent = intent_data.get("intent")
        admin_phone = os.getenv("ADMIN_PHONE")

        # 1. Marketing & BI (P21, P24)
        if intent == "MARKETING_APP" and phone == admin_phone:
            from experience.marketing_flows_service import MarketingFlowsService
            await MarketingFlowsService().trigger_marketing_dashboard(phone)
            return True

        # 2. Vendas & Comercial (P19, P20)
        if intent == "NEGOTIATION":
            from commerce.negotiation_service import NegotiationService
            res = await NegotiationService().negotiate(phone, message, 500.0)
            cloud_api.send_text_message(phone, res)
            return True

        if intent == "LOYALTY_STATUS":
            from marketing.loyalty_service import LoyaltyService
            msg = await LoyaltyService().get_status_message(phone)
            cloud_api.send_text_message(phone, msg)
            return True

        # 3. Clínica & Inteligência (P17, P22)
        if intent == "MINDMAP":
            from ai.meeting_intel_service import MeetingIntelService
            intel = await MeetingIntelService().process_consultation_transcript(message)
            cloud_api.send_text_message(phone, f"🧠 Insights: {intel.get('summary')}\n\n📍 Mermaid: {intel.get('mermaid_code')}")
            return True

        if intent == "MEDICAL_INFO" and phone == admin_phone:
            from ai.medical_engine import MedicalIntelService
            summary = await MedicalIntelService().get_patient_summary_for_doctor("5511988887777")
            cloud_api.send_text_message(phone, f"🏥 Briefing Clínico: {summary}")
            return True

        # 4. Outros Projetos (P9, P18, P25)
        if intent == "POP_CREATE" and phone == admin_phone:
            from compliance.pop_service import POPArchitectService
            res = await POPArchitectService().start_5w2h_interrogation(message)
            cloud_api.send_text_message(phone, res)
            return True

        if intent == "OUTREACH_START" and phone == admin_phone:
            from marketing.outreach_service import OutreachService
            await OutreachService().scan_and_trigger_outreach()
            cloud_api.send_text_message(phone, "🏹 Busca ativa iniciada com sucesso.")
            return True

        # Interceptação Global 360º de Tráfego Pago (Projeto 13 Expandido)
        if intent == "GLOBAL_ROAS" and phone == admin_phone:
             from marketing.omni_ads.manager import OmniAdsManager
             print(f"🌍 [BACKGROUND] Extraindo Dashboard Executivo Multi-Plataformas...")
             omni_ads = OmniAdsManager()
             flash_report = await omni_ads.get_global_roas_report()
             cloud_api.send_text_message(phone, f"📊 *RAIO-X DE PERFORMANCE OMNI (24H)*\n\n{flash_report}")
             return True

        if intent == "GOOGLE_ADS":
             # Mantido o fallback se a pessoa pedir SÓ Google no Orquestrador antigo
             import os
             if phone == os.getenv("ADMIN_PHONE"):
                  from marketing.ads_service import GoogleAdsService
                  print(f"🎯 [BACKGROUND] Solicitação Específica de Google Ads para o Admin {phone}...")
                  ads_service = GoogleAdsService()
                  suggestion = await ads_service.analyze_and_suggest("MOCK_CUSTOMER_ID")
                  cloud_api.send_text_message(phone, f"🎯 *ANÁLISE GOOGLE ADS EXCLUSIVA:*\n\n{suggestion}")
                  return True

        return False

import logging
from marketing.bi.data_analyst import DataAnalyst
from marketing.bi.executive_reporter import ExecutiveReporter
from database.repository import execute_raw_bi_query
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)
cloud_api = WhatsAppCloudClient()

class BIOrchestrator:
    """
    Orquestrador de Business Intelligence (Projeto 8).
    Coordena o fluxo entre a pergunta do dono, a execução SQL e a entrega do insight.
    """

    @classmethod
    async def process_bi_request(cls, phone: str, user_query: str):
        """
        Executa o pipeline completo de BI.
        """
        logger.info(f"📊 [BI ORCHESTRATOR] Iniciando análise para o Admin {phone}...")

        # --- NOVIDADE P21: DASHBOARD CONSOLIDADO ---
        if any(w in user_query.upper() for w in ["RESUMO", "DASHBOARD", "STATUS GERAL", "KPI"]):
            from marketing.bi.bi_executive_service import BIExecutiveService
            bi_service = BIExecutiveService()
            report = await bi_service.get_ceo_flash_report()
            cloud_api.send_text_message(phone, report)
            return True

        try:
            # 1. Traduzir pergunta em SQL
            sql_query = DataAnalyst.generate_sql(user_query)
            
            if not sql_query:
                cloud_api.send_text_message(phone, "❌ Não consegui traduzir sua pergunta em uma consulta de dados. Pode reformular?")
                return False

            logger.info(f"🔍 [BI ORCHESTRATOR] Executando SQL: {sql_query}")

            # 2. Executar no Banco de Dados Real
            raw_data = execute_raw_bi_query(sql_query)

            # 3. Formatar Resposta Executiva
            insight = ExecutiveReporter.format_insight(raw_data, user_query)

            # 4. Enviar ao Dono via WhatsApp
            cloud_api.send_text_message(phone, insight)
            return True

        except Exception as e:
            logger.error(f"❌ [BI ORCHESTRATOR ERROR] {e}")
            cloud_api.send_text_message(phone, "Oi Chefe, tivemos um erro técnico ao processar seu relatório. Já estamos ajustando.")
            return False

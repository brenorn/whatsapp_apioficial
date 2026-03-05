import logging
import os
from datetime import datetime
from ai.main_brain import generate_ai_response
from database.repository import is_ai_paused_for_phone, log_message
from core.whatsapp_cloud_client import WhatsAppCloudClient
from core.guardrails_manager import GuardrailsManager
from core.interceptors_manager import InterceptorsManager
from ai.intent_analyzer import IntentAnalyzer
from ai.rag_manager import RAGManager

logger = logging.getLogger(__name__)
cloud_api = WhatsAppCloudClient()

async def manage_incoming_message(phone: str, message: str, msg_type: str = "text", media_id: str = None, order_data: dict = None):
    """
    Orquestrador Central Modular (Padrão Sênior).
    Gerencia Segurança (Guardrails), Roteamento (Interceptors) e IA.
    """
    print(f"🔄 [ORCHESTRATOR] Processando {phone} ({msg_type})")
    
    # 1. Filtro de Handoff
    if is_ai_paused_for_phone(phone):
         return None

    # 2. Guardrails de Entrada (Lógica Pura / Segurança)
    guard = GuardrailsManager.validate_input(message)
    if guard["status"] == "BLOCKED":
        cloud_api.send_text_message(phone, "Conteúdo bloqueado por segurança.")
        return None

    # 3. Interceptadores de Mídia (Imagens/Vídeos - P15)
    if msg_type in ["image", "video"] and media_id:
        from marketing.social.social_command_center import SocialCommandCenter
        local_path = cloud_api.download_media(media_id)
        if local_path and msg_type == "video":
            from video.video_service import VideoAutoEditorService
            await VideoAutoEditorService().process_video_reels(local_path)
            cloud_api.send_text_message(phone, "✅ Vídeo em processamento...")
        return None

    # 4. Logs e Intent Analysis
    log_message(phone, message, sender="user", msg_type=msg_type)
    
    # IA Engine: Auto-Alimentação de Conhecimento (GraphRAG Style)
    import asyncio
    asyncio.create_task(RAGManager.extract_and_feed_graph(message))
    
    intent_data = IntentAnalyzer.identify_intent(message)

    # 5. Roteamento de Projetos (Interceptors P9-P25)
    # Movemos toda a lógica de IFs gigantes para o InterceptorsManager
    if await InterceptorsManager.process_intent(phone, message, intent_data, cloud_api):
        return None

    # 6. Fluxos de Pagamento e Carrinho (P1)
    if msg_type == "order" and order_data:
        from commerce.order_processor import OrderProcessor
        res = OrderProcessor.process_incoming_order(phone, order_data)
        cloud_api.send_text_message(phone, res.get('pix_br_code', "Erro financeiro."))
        return None

    # 7. Resposta via IA com Guardrails de Saída
    print(f"🧠 [IA] Gerando resposta para {phone}...")
    ai_response_raw = generate_ai_response(message, phone)
    
    # Higiene e Proteção de Dados na Saída
    ai_response = GuardrailsManager.validate_output(ai_response_raw, context="General")
    
    log_message(phone, ai_response, sender="bot")
    cloud_api.send_text_message(phone, ai_response)


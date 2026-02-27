import json
import logging
from database.repository import log_message
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)
cloud_api = WhatsAppCloudClient()

class BookingProcessor:
    """
    Processador de Agendamentos (Módulo de Experiência).
    Responsável por decodificar o JSON vindo do WhatsApp Flows e 
    persistir a consulta no banco de dados.
    """

    @classmethod
    def process_flow_response(cls, phone: str, raw_message: str) -> bool:
        """
        Detecta se a mensagem é um payload de formulário e processa.
        """
        if "📅 [FORMULÁRIO_AGENDA_PREENCHIDO]:" not in raw_message:
            return False

        try:
            # Extrair o JSON da string formatada pelo parser
            json_str = raw_message.split("📅 [FORMULÁRIO_AGENDA_PREENCHIDO]:")[1].strip()
            data = json.loads(json_str)
            
            # Aqui simulamos a persistência (ex: salva na tabela de appointments)
            # No futuro: appointment_service.create(phone, data['date'], data['slot'])
            logger.info(f"✅ [BOOKING PROCESSOR] Agendamento Recebido para {phone}: {data}")
            
            # 1. Logar no banco como uma ação de sistema
            log_message(phone, f"📝 AGENDAMENTO CONFIRMADO: {data.get('date', 'N/A')} às {data.get('time', 'N/A')}", sender="bot")
            
            # 2. Enviar confirmação visual ao cliente
            confirmacao = (
                f"✅ *Agendamento Confirmado!*\n\n"
                f"📅 *Data:* {data.get('date', '---')}\n"
                f"⏰ *Horário:* {data.get('time', '---')}\n"
                f"📍 *Local:* Clínica MoveMind\n\n"
                f"Já deixamos tudo pronto por aqui. Se precisar mudar algo, é só avisar!"
            )
            cloud_api.send_text_message(phone, confirmacao)
            
            return True

        except Exception as e:
            logger.error(f"❌ [BOOKING PROCESSOR] Erro ao processar payload do Flow: {e}")
            cloud_api.send_text_message(phone, "Recebemos seus dados, mas houve um erro ao processar o agendamento. Nossa secretária entrará em contato.")
            return True # Retorna True para interromper o fluxo da IA mesmo com erro controlado

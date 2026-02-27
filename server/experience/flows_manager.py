import os
import logging
from core.whatsapp_cloud_client import WhatsAppCloudClient

logger = logging.getLogger(__name__)
cloud_client = WhatsAppCloudClient()

class FlowsManager:
    """
    Microserviço de Experiência (Agenda In-App).
    Em vez da IA Principal fazer dezenas de perguntas ao usuário ("CEP", "Dia", "Hora"), 
    o FlowsManager é acionado para injetar no WhatsApp uma U.I Nativa (Formulário Visual).
    A Meta desenha o app no celular do paciente e devolve um JSON final.
    """
    
    # Este ID vem do seu painel do Meta Business Manager (WhatsApp Manager > Flows)
    # Como não temos um fixo neste teste RAG, usamos um placeholder seguro.
    CLINICA_FLOW_ID = os.getenv("META_AGENDA_FLOW_ID", "1234567890_placeholder")

    @classmethod
    def trigger_schedule_flow(cls, phone: str) -> bool:
        """
        [P3.3] Envia o convite do formulário. A tela do celular do cliente agora terá 
        um botão "Agendar Horário" que, ao ser clicado, abre o mini-aplicativo da clínica.
        """
        logger.info(f"📅 [FLOWS MANAGER] Detectada Intenção de Agendamento. Acionando Form Meta para o Lead {phone}.")
        
        # Mensagem-Mestra convidativa gerada baseada em técnicas de TTR (Time to Resolution)
        body_text = (
            "🎯 Excelente decisão! Para agilizarmos e garantir a sua vaga na agenda, "
            "clique no botão abaixo.\n\n"
            "Ele abrirá um calendário rápido e seguro na sua tela para você escolher o dia perfeito."
        )
        
        # Cria a ação do Flow a ser enviada pro Cloud API
        interactive_object = {
            "type": "flow",
            "header": {
                "type": "text",
                "text": "Agendamento Inteligente"
            },
            "body": {
                "text": body_text
            },
            "footer": {
                "text": "MoveMind Health 🔒"
            },
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",  # Versão oficial atualizada da Meta
                    "flow_token": f"FLOW_TOKEN_{phone}",
                    "flow_id": cls.CLINICA_FLOW_ID,
                    "flow_cta": "Visualizar Calendário",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "AGENDAMENTO_HOME", # Primeira tela do form
                        "data": {
                            "phone_number": phone
                        }
                    }
                }
            }
        }
        
        return cloud_client.send_interactive_flow(phone, interactive_object)

from typing import List, Dict

def parse_meta_payload(payload: dict) -> List[Dict]:
    """
    Função de Extracao Robusta de JSON (Versão Sênior/Lista).
    Trata múltiplos eventos em um lote e distingue "Mensagens" de "Recibos de Leitura".
    """
    results = []
    try:
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                
                # 1. PROCESSAR STATUSES (Recibos de Lida/Entregue)
                if "statuses" in value:
                    for status_obj in value["statuses"]:
                        wamid = status_obj.get("id")
                        status_str = status_obj.get("status") # 'read', 'delivered', 'failed', 'sent'
                        phone = status_obj.get("recipient_id")
                        
                        results.append({
                            "is_status": True,
                            "is_message": False,
                            "wamid": wamid,
                            "status": status_str,
                            "phone": phone
                        })
                
                # 2. PROCESSAR MENSAGENS INBOUND (Lead falando)
                if "messages" in value:
                    for message_obj in value["messages"]:
                        sender_phone = message_obj.get("from")
                        msg_type = message_obj.get("type", "unknown")
                        
                        text = ""
                        media_id = None
                        
                        if msg_type == "text":
                            text = message_obj.get("text", {}).get("body", "")
                        elif msg_type == "audio":
                            media_id = message_obj.get("audio", {}).get("id")
                            text = f"🎙️ [ÁUDIO: {media_id}]"
                        elif msg_type == "image":
                            media_id = message_obj.get("image", {}).get("id")
                            caption = message_obj.get("image", {}).get("caption", "")
                            text = f"📷 [IMAGEM: {media_id}] {caption}".strip()
                        elif msg_type == "document":
                            media_id = message_obj.get("document", {}).get("id")
                            text = f"📄 [DOCUMENTO: {media_id}]"
                        elif msg_type == "button":
                           # O lead clicou num botão enviado previamente
                           text = message_obj.get("button", {}).get("text", "")
                        elif msg_type == "interactive":
                            # Botões tipo Reply de Lista ou Formulários do Flows (Módulo 3)
                           interactive_type = message_obj.get("interactive", {}).get("type")
                           if interactive_type == "button_reply":
                               text = message_obj["interactive"]["button_reply"]["title"]
                           elif interactive_type == "list_reply":
                               text = message_obj["interactive"]["list_reply"]["title"]
                           elif interactive_type == "nfm_reply":
                               # Payload do Mini-App (Flows)
                               response_json = message_obj["interactive"]["nfm_reply"].get("response_json", "{}")
                               text = f"📅 [FORMULÁRIO_AGENDA_PREENCHIDO]: {response_json}"
                        elif msg_type == "order":
                            # Evento de Carrinho de Compras do E-commerce App Whatsapp
                            order_details = message_obj.get("order", {})
                            text = "🛍️ [CARRINHO DE COMPRAS RECEBIDO]"
                            order_data = order_details
                        else:
                            print(f"⚠️ [IGNORANDO] Mensagem tipo {msg_type} de {sender_phone} não suportada na V2.")
                            continue
                            
                        results.append({
                            "is_message": True,
                            "is_status": False,
                            "phone": sender_phone,
                            "message_text": text,
                            "msg_type": msg_type,
                            "media_id": media_id,
                            "order_data": order_data if msg_type == "order" else None
                        })
                        
    except Exception as e:
        print(f"❌ [PARSER ERROR] Nao foi possivel raspar lote: {e}")
        
    return results

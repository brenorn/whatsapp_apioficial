import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Header
from fastapi.responses import PlainTextResponse, JSONResponse
from core.webhook_parser import parse_meta_payload
from core.orchestrator import manage_incoming_message
from core.whatsapp_cloud_client import WhatsAppCloudClient
from database.repository import log_message, update_message_status
from core.security import validate_hub_signature

app = FastAPI(title="MoveMind WhatsApp Core API")
cloud_api = WhatsAppCloudClient()

VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN", "movemind_secure_token")
# Desligar verificação se em MOCK local (sem tunnel) mas usar True em prod
REQUIRE_SIGNATURE = os.getenv("REQUIRE_SIGNATURE", "false").lower() == "true"

@app.get("/webhook/meta")
async def handshake(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Rota de Validação e Handshake Exclusiva da Meta."""
    mode = hub_mode or ""
    token = hub_verify_token or ""
    challenge = hub_challenge or ""

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ [AUTH] Webhook verificado pela Meta no painel Developer!")
        return PlainTextResponse(challenge, status_code=200)
    elif mode or token:
        print(f"❌ [AUTH] Token Inválido: {token} recebido.")
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return JSONResponse({"status": "API Online & Handoff Pronta"}, 200)


@app.post("/webhook/meta")
async def webhook_stream(request: Request, background_tasks: BackgroundTasks):
    """
    Assíncrono: Retorna 200 OK imediato e empurra a IA pro BackgroundTasks.
    Impede timeout da Meta e estrangulamento.
    """
    raw_payload = await request.body()
    signature = request.headers.get("x-hub-signature-256", "")

    # 1. Blindagem: Validação Zero-Trust
    if REQUIRE_SIGNATURE:
        if not validate_hub_signature(raw_payload, signature):
            print("🦊 [SECURITY] Assinatura HMAC rejeitada. Requisicao Hacker bloqueada.")
            raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        body = await request.json()
        print(f"📡 Payload Inbound Recebido.")
        
        # 2. O Parser lida c/ Status, Textos, Images e Audio
        extracted_data_list = parse_meta_payload(body)
        
        # 3. Empilhar as tarefas em Background
        if extracted_data_list:
            for item in extracted_data_list:
                # Se for mensagem legível
                if item.get("is_message"):
                    background_tasks.add_task(
                        manage_incoming_message,
                        item.get("phone"), 
                        item.get("message_text"),
                        item.get("msg_type"),
                        item.get("media_id"),
                        item.get("order_data")
                    )
                # Se for aviso de leitura (Read Receipt)
                elif item.get("is_status"):
                    background_tasks.add_task(
                        update_message_status,
                        item.get("wamid"),
                        item.get("phone"),
                        item.get("status") # sent, delivered, read, failed
                    )
                    
        # Retorna IMEDIATAMENTE antes da Background_Task Sequencial ligar o LLM.
        return JSONResponse({"status": "success"}, 200)

    except Exception as e:
        print(f"💥 [ERRO GRAVE] Falha Fatal: {str(e)}")
        # Mesmo com erro, devolve 200 para a Meta não ficar retentando eternamente payloads corrompidos.
        return JSONResponse({"status": "error_handled", "error": str(e)}, 200)


@app.post("/api/send")
async def send_manual_message(request: Request):
    """Endpoint M2M (Node JS -> Python)."""
    try:
        data = await request.json()
        phone = data.get("phone")
        message = data.get("text")
        
        success = cloud_api.send_text_message(phone, message)
        if success:
            # Trava o LLM imediatamente (The Golden Rule)
            log_message(phone, message, sender="me")
            return JSONResponse({"status": "success"}, 200)
        else:
            raise HTTPException(status_code=500, detail="Meta Graph API Failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import os
import requests

class WhatsAppCloudClient:
    """Ferramenta HTTP especializada em interacoes POST/GET com Graph API Meta"""
    
    def __init__(self):
        self.api_version = "v21.0"
        self.access_token = os.getenv("META_API_TOKEN")
        self.phone_number_id = os.getenv("PHONE_NUMBER_ID")
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def send_text_message(self, to_phone: str, text: str) -> bool:
        """Envia texto cru."""
        if not self.access_token or not self.phone_number_id:
            print("⚠️ [MOCK CLOUD] Token/Phone ID ausentes. Log apenas local.")
            return True

        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": text
            }
        }
        
        return self._do_post(url, payload)

    def send_action(self, to_phone: str, action: str) -> bool:
        """'typing_on', 'typing_off', 'read'"""
        action_map = {
            "typing": "typing_on", "typing_on": "typing_on",
            "typing_off": "typing_off"
        }
        if action not in action_map: return False
        
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",  # ironicamente, typing status não vai no 'type', mas na estrutura raiz
        }
        
        # Correção estrutura oficial de typing da Meta API (v20+)
        typing_payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            # A Meta não tem nativamente typing_on no Graph API Core como na Evolution.
            # Esta função fica como stub futuro para compatibilidade se eles liberarem pro Brasil.
        }
        return False
        
    def download_media(self, media_id: str) -> str:
        """
        1. Bate na API da Meta pra pegar a URL de download via media_id
        2. Bate na URL de download com Bearer e baixa o binario.
        """
        try:
            # Pega a URL Real
            url_info = f"https://graph.facebook.com/{self.api_version}/{media_id}"
            resp_info = requests.get(url_info, headers=self.get_headers(), timeout=10)
            if resp_info.status_code != 200:
                print(f"❌ [MEDIA INFO] Falha na URL: {resp_info.text}")
                return None
                
            download_url = resp_info.json().get("url")
            
            # Baixa o binário
            resp_file = requests.get(download_url, headers=self.get_headers(), stream=True, timeout=15)
            if resp_file.status_code == 200:
                # Salvar temporariamente num diretório local
                os.makedirs("temp_media", exist_ok=True)
                filepath = f"temp_media/{media_id}.ogg" # Assume OGG para Audio inicial
                with open(filepath, 'wb') as f:
                    for chunk in resp_file.iter_content(1024):
                        f.write(chunk)
                return filepath
                
            return None
        except Exception as e:
            print(f"❌ [MEDIA DOWNLOAD ERROR] {e}")
            return None
            
    def send_interactive_buttons(self, to_phone: str, body_text: str, buttons: list) -> bool:
        """
        Envia botões nativos para Fast Path Decisions (BMAD methodology).
        `buttons` = [{"id": "btn_yes", "title": "Sim"}, {"id": "btn_no", "title": "Não"}]
        """
        formatted_buttons = []
        for btn in buttons:
            formatted_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn["id"],
                    "title": btn["title"][:20]  # Meta limita a 20 caracteres
                }
            })

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": formatted_buttons}
            }
        }
        
        return self._do_post(f"{self.base_url}/messages", payload)

    def send_product_message(self, to_phone: str, catalog_id: str, product_retailer_id: str, body_text: str = "Temos isso disponíveis para você!") -> bool:
        """
        Aciona a Vitrine: Mostra um produto específico permitindo o "Adicionar ao Carrinho".
        Exige o `catalog_id` e o `product_retailer_id` gerados no Meta Commerce Manager.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "product",
                "body": {"text": body_text},
                "action": {
                    "catalog_id": catalog_id,
                    "product_retailer_id": product_retailer_id
                }
            }
        }
        
        return self._do_post(f"{self.base_url}/messages", payload)
        
    def send_interactive_flow(self, to_phone: str, interactive_object: dict) -> bool:
        """
        [P3.3] Envia um Meta Flow (Mini-App / Formulário) para a tela do usuário.
        O objeto Interactive constrói a UI de botões na raiz do Whatsapp In-App.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            "interactive": interactive_object
        }
        return self._do_post(f"{self.base_url}/messages", payload)
        
    def send_template_message(self, to_phone: str, template_name: str, language_code: str = "pt_BR", components: list = None) -> bool:
        """
        [P5.1] Envia uma mensagem baseada em Template (HSM).
        Única forma de iniciar conversas ativas (Broadcast/Recaptura) permitida pela Meta.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
            
        return self._do_post(f"{self.base_url}/messages", payload)

    def _do_post(self, url: str, json_data: dict) -> bool:
        try:
            resp = requests.post(url, headers=self.get_headers(), json=json_data, timeout=10)
            if resp.status_code in [200, 201]:
                return True
            else:
                print(f"❌ [FACEBOOK ERRO] {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            print(f"❌ [HTTP FAIL] {e}")
            return False

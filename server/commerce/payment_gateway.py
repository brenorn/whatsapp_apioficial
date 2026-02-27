import os
import uuid
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PaymentGateway:
    """
    Microsserviço Transacional: Integração com BaaS (Banking as a Service).
    Gera cobranças dinâmicas (PIX) para Ordens Recebidas do WhatsApp.
    O padrão BMAD dita que chaves de API Financeiras devem ser estritamente puxadas do .env
    e os UUIDs (TxID) devem ser únicos por carrinho.
    """
    
    # Exemplo focado na Efí Bank (Antiga Gerencianet) ou Mercado Pago, 
    # mantemos agnóstico via Interface.
    PIX_KEY = os.getenv("PIX_DICT_KEY", "chave-pix-padrao@clinica.com.br")
    MERCHANT_NAME = os.getenv("MERCHANT_NAME", "MoveMind Oficial")
    MERCHANT_CITY = os.getenv("MERCHANT_CITY", "Sao Paulo")
    
    @classmethod
    def generate_pix_charge(cls, total_amount: float, order_id: str) -> Dict[str, str]:
        """
        Gera um PIX BR-Code (Copia e Cola) válido segundo normas do BACEN.
        Se houve integração com Pagar.me/Efí, a chamada HTTP POST iria aqui.
        Como Boilerplate, geraremos a Payload BR-Code EMULADA para testes, 
        mas com a arquitetura preparada para injeção de API Real.
        """
        try:
            # txid deve ser unico. Usaremos o wamid ou um uuid truncado.
            txid = f"PEDIDO{order_id[:8].upper()}"
            amount_str = f"{total_amount:.2f}"
            
            logger.info(f"🏦 [PAYMENT GATEWAY] Gerando Cobrança PIX. Valor: R$ {amount_str} | TxID: {txid}")
            
            # --- MOCK DA INTEGRAÇÃO REAL (API REST) ---
            # Em prod: requests.post('api.efi.com.br/v2/loc', cert='certificado.pem', json={'tipoCob': 'pix'})
            
            # Gerador Estático de BR-Code (Exemplo Visual para o Cliente)
            # O PayloadBR nativo exige CRC16, aqui usamos uma string mock representativa
            # para o front-end ou para a API enviar.
            mock_br_code = f"00020126580014br.gov.bcb.pix0136{cls.PIX_KEY}520400005303986540{len(amount_str):02d}{amount_str}5802BR5915{cls.MERCHANT_NAME[:15]}6015{cls.MERCHANT_CITY[:15]}62180514{txid}6304"
            
            # Mock de URL de QR Code Dinamico gerado pela API Financeira
            mock_qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={mock_br_code}"
            
            return {
                "status": "success",
                "txid": txid,
                "br_code": mock_br_code,       # O famoso Copia e Cola
                "qr_url": mock_qr_image_url,   # Imagem para o client WhatsApp baixar
                "amount": amount_str
            }
            
        except Exception as e:
            logger.error(f"❌ [PAYMENT GATEWAY] Erro Fatal na geração do PIX: {e}")
            return {"status": "error", "message": "Falha na comunicação com o Banco."}

    @classmethod
    def verify_payment_status(cls, txid: str) -> bool:
        """
        Consultaria o Endpoint de Webhook Financeiro para liberar 
        a entrega/agendamento no Orquestrador.
        """
        # Em prod: requests.get(f'/v2/pix/{txid}') -> status == 'CONCLUIDA'
        return False

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OrderProcessor:
    """
    Processador de Carrinho de Compras (Shopping Cart).
    Recebe os Webhooks do tipo 'order' enviados nativamente pelo WhatsApp 
    e traduz para o Checkout/ERP ou Sistema Financeiro.
    """
    
    @classmethod
    def process_incoming_order(cls, phone: str, order_data: Dict[Any, Any]):
        """
        Lê o carrinho submetido pelo paciente/lead.
        O order_data vem do `webhook_parser` e contém a lista de itens e soma.
        """
        try:
            logger.info(f"🛒 [CHECKOUT] Nova ordem recebida do Lead {phone}.")
            
            catalog_id = order_data.get("catalog_id")
            product_items = order_data.get("product_items", [])
            total_price = 0.0
            currency = ""
            
            summary = []
            
            for item in product_items:
                p_id = item.get("product_retailer_id")
                qty = item.get("quantity", 1)
                item_price = float(item.get("item_price", 0))
                currency = item.get("currency", "BRL")
                
                sum_item = qty * item_price
                total_price += sum_item
                
                summary.append(f"{qty}x Produto {p_id} (Und: {currency} {item_price})")
                
            logger.info(f"💵 [CARRINHO DETALHES] {summary}. Total Calculado: {currency} {total_price}")
            
            # TODO: Gerar UUID rastreavel real do BD no futuro
            order_fake_id = phone[-4:] + "X99" 
            
            # 1. Bater no novo Microsserviço de Pagamento
            from commerce.payment_gateway import PaymentGateway
            payment_info = PaymentGateway.generate_pix_charge(total_price, order_id=order_fake_id)
            
            if payment_info["status"] == "error":
                return {"status": "order_failed", "message": payment_info.get("message")}
            
            # 2. Notificar Meta Ads (CAPI Tracker - Projeto 4)
            from marketing.capi_tracker import CAPITracker
            CAPITracker.track_purchase(phone, total_price, currency, order_id=payment_info.get("txid"))

            return {
                "status": "order_received",
                "total": total_price,
                "currency": currency,
                "items": len(product_items),
                "pix_br_code": payment_info["br_code"],
                "pix_qr_url": payment_info["qr_url"],
                "txid": payment_info["txid"]
            }
            
        except Exception as e:
            logger.error(f"❌ [ORDER FATAL] Falha processando carrinho: {e}")
            return {"status": "order_failed"}

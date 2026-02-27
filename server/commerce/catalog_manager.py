import os
import requests
import logging

logger = logging.getLogger(__name__)

class CatalogManager:
    """
    Controlador Mestre do Meta Commerce Manager (Catálogo B2B/B2C).
    BMAD Methodology: A fonte da verdade (SSOT) dos produtos é sempre
    o servidor da Meta ou um ERP sincronizado bidirecionalmente.
    """
    
    def __init__(self):
        self.api_version = "v21.0"
        self.access_token = os.getenv("META_API_TOKEN")
        self.catalog_id = os.getenv("META_CATALOG_ID", "LACKING_CATALOG_ID") # Set no .env
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.catalog_id}"

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def fetch_products(self) -> list:
        """
        Consulta todos os produtos ativos no Catálogo da Meta.
        Útil para o AI RAG saber o que pode ser vendido hoje (Estoque/Precificação).
        """
        if not self.access_token or self.catalog_id == "LACKING_CATALOG_ID":
            logger.warning("⚠️ [Commerce API] Catalog ID ou Token ausentes. Mock mode ativo.")
            return []

        url = f"{self.base_url}/products"
        try:
            resp = requests.get(url, headers=self.get_headers(), timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", [])
            else:
                logger.error(f"❌ [Commerce API] Erro ao buscar catálogo: {resp.text}")
                return []
        except Exception as e:
            logger.error(f"❌ [HTTP FAIL] Catalog Request Error: {e}")
            return []

    def format_product_for_llm(self, product_data: dict) -> str:
        """
        Formata o JSON bruto da Graph API num String compacto para RAG do Gemini.
        Padrão Mínimo: ID, NOME, DESCRIÇÃO, PREÇO.
        """
        # Estrutura baseada em Product Item Object da Graph API
        pid = product_data.get("id", "N/A")
        name = product_data.get("name", "N/A")
        desc = product_data.get("description", "N/A")
        price = product_data.get("price", "N/A")
        currency = product_data.get("currency", "BRL")
        
        return f"Produto: {name} | ID Oficial: {pid} | Valor: {currency} {price}\nDetalhes: {desc}"

catalog_manager = CatalogManager()

import logging
import json
from typing import List, Dict, Any
from ai.llm_factory import LLMFactory
from ai.graph_engine import graph_engine
from database.repository import execute_raw_bi_query

logger = logging.getLogger(__name__)

class RAGManager:
    """
    Orquestrador HybridRAG MoveMind (Inspirado em Sandeco).
    Funde dados Relacionais (SQL), Conexões (Graph) e Conteúdo (Vector/RAG).
    """

    @classmethod
    async def hybrid_query(cls, user_query: str, phone: str = None) -> str:
        """
        Realiza uma busca multivariada para dar o contexto mais rico possível para a IA.
        """
        logger.info(f"🧬 [HYBRID RAG] Iniciando busca profunda para: {user_query}")

        # 1. Busca no Grafo (Neo4j) - Relacionamentos e Entidades
        # (Ex: Sintomas relacionados ou conexões familiares/jurídicas)
        graph_context = graph_engine.get_related_nodes(user_query)
        
        # 2. Busca no SQL (Postgres) - Dados Transacionais e Histórico
        # (Ex: Últimas consultas, compras ou mensagens)
        sql_context = []
        if phone:
            sql_query = f"SELECT message FROM whatsapp_messages WHERE phone = '{phone}' ORDER BY created_at DESC LIMIT 5"
            sql_context = execute_raw_bi_query(sql_query)

        # 3. Prompt de Fusão de Contexto
        full_context = f"""
        CONTEXTO DE GRAFO (Conexões): {graph_context}
        CONTEXTO TRANSACIONAL (SQL): {sql_context}
        """

        logger.info("✅ [HYBRID RAG] Contexto fundido com sucesso.")
        
        return full_context

    @classmethod
    async def extract_and_feed_graph(cls, text: str):
        """
        Motor de 'Auto-Alimentação' do Grafo.
        Extrai entidades do chat e injeta no Neo4j em tempo real.
        """
        prompt = f"""
        Aja como um Extrator de Entidades GraphRAG.
        Analise o texto abaixo e extraia Relações no formato JSON:
        {{ "entities": ["ENTIDADE1", "ENTIDADE2"], "relations": [["ENTIDADE1", "RELACAO", "ENTIDADE2"]] }}
        
        Texto: "{text}"
        """
        
        try:
            response = LLMFactory.generate(prompt, task_level="complex")
            # Limpeza e Safe Parse
            data = cls._parse_extraction(response)
            
            if data and "relations" in data:
                for rel in data["relations"]:
                    if len(rel) == 3:
                        graph_engine.add_clinical_connection(rel[0], rel[2])
                        
            logger.info("🕸️ [AUTO-FEED] Grafo atualizado com novos neurônios de conhecimento.")
        except Exception as e:
            logger.error(f"❌ [AUTO-FEED] Falha na extração de grafo: {e}")

    @staticmethod
    def _parse_extraction(text: str) -> Dict:
        import re
        try:
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return {}
        except:
            return {}

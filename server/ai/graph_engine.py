import os
import logging
from typing import List, Dict, Any

try:
    from neo4j import GraphDatabase
    HAS_NEO4J = True
except ImportError:
    HAS_NEO4J = False

logger = logging.getLogger(__name__)

class GraphEngine:
    """
    Motor de Grafos MoveMind (Neo4j).
    Responsável por mapear as relações de 'Conhecimento Profundo'.
    P22 (Saúde), P17 (Jurídico), P11 (Groups).
    """

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASS", "movemind_secret")
        self.driver = None
        
        if HAS_NEO4J:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            except Exception as e:
                logger.error(f"❌ Falha ao conectar no Neo4j: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def add_clinical_connection(self, symptom: str, potential_diagnosis: str):
        """Mapeia correlações para o Health Vault (P22)."""
        if not self.driver: return
        query = """
        MERGE (s:Symptom {name: $symptom})
        MERGE (d:Diagnosis {name: $diagnosis})
        MERGE (s)-[:SUGERE]->(d)
        """
        with self.driver.session() as session:
            session.run(query, symptom=symptom, diagnosis=potential_diagnosis)
            logger.info(f"🕸️ [GRAPH] Conexão criada: {symptom} -> {potential_diagnosis}")

    def get_related_nodes(self, node_name: str) -> List[str]:
        """Busca conexões para injetar no contexto da IA (RAG de Grafos)."""
        if not self.driver: return []
        query = """
        MATCH (n {name: $name})-->(related)
        return related.name as name
        """
        with self.driver.session() as session:
            result = session.run(query, name=node_name)
            return [record["name"] for record in result]

# Instância Singleton
graph_engine = GraphEngine()

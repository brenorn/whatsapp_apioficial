import logging
import asyncio
from typing import List, Dict, Any
from ai.knowledge_vault.engines.entities_extractor import EntitiesExtractor
from ai.knowledge_vault.engines.graph_aggregator import GraphAggregator
from ai.knowledge_vault.engines.cypher_generator import CypherGenerator
from ai.graph_engine import graph_engine

logger = logging.getLogger(__name__)

class KnowledgeVaultOrchestrator:
    """
    Orquestrador Mestre de Conhecimento (GraphRAG + HybridRAG).
    Inspirado no sistema do Sandeco.
    Responsável por transformar textos brutos (livros/artigos) em Inteligência Estruturada.
    """

    DEFAULT_SCHEMA = {
        "tipos_entidade": {
            "PESSOA": {}, "ORGANIZACAO": {}, "LOCAL": {}, "CONCEITO": {}, 
            "MEDICAMENTO": {}, "SINTOMA": {}, "LEI": {}, "ORGAO": {}
        },
        "tipos_relacionamento": {
            "CONHECE": {}, "TRABALHA_EM": {}, "SITUADO_EM": {}, "SUGERE": {},
            "CONTRAINDICA": {}, "CITADO_EM": {}, "PERTENCE_A": {}, "CAUSA": {}
        }
    }

    @classmethod
    async def ingest_document(cls, text: str, area_name: str):
        """
        Lógica completa de ingestão: Texto -> Grafo -> Vetor.
        """
        logger.info(f"📚 [VAULT] Iniciando ingestão em '{area_name}'...")

        # 1. Chunking do Texto (Sandeco Style)
        # Chunks de 500 caracteres com overlap de 100
        chunks = cls._create_chunks(text, size=1000, overlap=200)
        
        extractor = EntitiesExtractor(schema_data=cls.DEFAULT_SCHEMA)
        aggregator = GraphAggregator()

        # 2. Extração Paralela/Serial de Entidades (Nível de Chunks)
        for i, chunk in enumerate(chunks):
            logger.info(f"🔄 [VAULT] Processando chunk {i+1}/{len(chunks)}...")
            extraction = extractor.extract(chunk)
            aggregator.add_extraction(extraction)
            # Pausa curta para evitar rate limit se necessário
            await asyncio.sleep(0.5)

        # 3. Consolidação Final (Snapshot)
        snapshot = aggregator.snapshot()
        logger.info(f"✅ [VAULT] Snapshot consolidado: {len(snapshot['entities'])} entidades encontradas.")

        # 4. Geração e Execução Cypher (Neo4j)
        generator = CypherGenerator()
        cypher_script = generator.generate(snapshot, domain=area_name)
        
        if graph_engine.driver:
            with graph_engine.driver.session() as session:
                # Executamos o script linha a linha ou em batch
                for line in cypher_script.split('\n'):
                    if line.strip():
                        session.run(line)
            logger.info(f"🕸️ [VAULT] Grafo Neo4j atualizado para área: {area_name}")
        else:
            logger.error("❌ [VAULT] Falha na conexão com Neo4j.")

        # 5. Indexação Vetorial (Opcional - Requer ChromaDB pronto)
        # TODO: Implementar vector_store.add_chunks(chunks, metadata={"area": area_name})

        return {
            "status": "success",
            "entities_found": len(snapshot["entities"]),
            "area": area_name
        }

    @staticmethod
    def _create_chunks(text: str, size: int, overlap: int) -> List[str]:
        chunks = []
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i : i + size])
        return chunks

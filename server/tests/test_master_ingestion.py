import asyncio
import sys
import os

# Ajuste de path para importar o server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.knowledge_vault.vault_orchestrator import KnowledgeVaultOrchestrator

async def test_full_document_ingestion():
    """
    Simula o caso de uso: Usuário envia um texto longo (artigo)
    e pede para inserir na área 'MEDICINA_ESPORTIVA'.
    """
    
    artigo_exemplo = """
    A Creatina é um dos suplementos mais estudados na nutrição esportiva. 
    Ela é sintetizada naturalmente pelo corpo humano nos rins e fígado. 
    O uso de Creatina Monohidratada auxilia na ressíntese de ATP, aumentando a força muscular.
    Estudos indicam que o Dr. Sandeco recomenda o uso cíclico para atletas de alto rendimento.
    No entanto, o uso é contraindicado para pessoas com insuficiência renal crônica.
    A ANVISA regula a comercialização deste suplemento no Brasil.
    """

    print("\n🚀 [TESTE INGESTÃO] Iniciando Processamento de Artigo...")
    
    result = await KnowledgeVaultOrchestrator.ingest_document(
        text=artigo_exemplo, 
        area_name="MEDICINA_ESPORTIVA"
    )

    print(f"\n✅ RESULTADO: {result}")
    print("\nVerifique seu Neo4j Browser: MATCH (n:MEDICINA_ESPORTIVA) RETURN n")

if __name__ == "__main__":
    asyncio.run(test_full_document_ingestion())

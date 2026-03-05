import asyncio
import os
import sys
import logging

# Configuração de Path para importar os módulos do server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.bi_orchestrator import BIOrchestrator
from core.config_manager import BusinessConfigManager

# Configurar logging para ver o que a IA está pensando
logging.basicConfig(level=logging.INFO)

async def test_executive_bi():
    """
    Teste offline do Cérebro BI (P8).
    Simula o CEO perguntando sobre o faturamento e performance.
    """
    print("\n📊 [TESTE BI] Iniciando Auditoria de Inteligência de Dados...")

    # Cenário: Clínica deseja saber sobre leads
    questions = [
        "Qual o valor total de negociações ganhas este mês?",
        "Quantas mensagens os pacientes enviaram hoje?",
        "Qual a média de score NPS dos nossos atendimentos?"
    ]

    for q in questions:
        print(f"\n🙋 CEO pergunta: '{q}'")
        response = await BIOrchestrator.ask_data(q)
        print(f"🤖 Resposta da IA:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_executive_bi())

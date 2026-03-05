import asyncio
import os
import yaml
from ai.llm_factory import LLMFactory
from commerce.negotiation_service import NegotiationService
from core.config_manager import BusinessConfigManager

async def test_agnostic_transmutation():
    """
    Demonstração da 'Transmutação' do Sistema entre dois setores.
    Mesmo código, comportamentos completamente diferentes baseados no YAML.
    """
    negotiator = NegotiationService()
    objection = "Está muito caro, não consigo pagar esse valor agora."
    
    # --- CENÁRIO 1: CLÍNICA MÉDICA ---
    print("\n🏥 [CENÁRIO 1: CLÍNICA MÉDICA]")
    profile_med = {
        "company_name": "MoveMind Health",
        "sector": "Medicina/Clínica",
        "tone_of_voice": "Empático e Técnico",
        "customer_label": "Paciente",
        "core_service_label": "Tratamento",
        "critical_rules": ["Segurança do paciente em primeiro lugar"],
        "ai_persona": "Você é um Consultor de Saúde Sênior."
    }
    with open("server/business_profile.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(profile_med, f)
    
    res_med = await negotiator.negotiate("5511999999999", objection, 1500.0)
    print(f"🤖 Resposta IA (Modo Médico):\n{res_med}\n")

    # --- CENÁRIO 2: ESCRITÓRIO DE ADVOCACIA ---
    print("⚖️ [CENÁRIO 2: ADVOCACIA]")
    profile_legal = {
        "company_name": "MoveMind Legal Services",
        "sector": "Advocacia/Jurídico",
        "tone_of_voice": "Formal, Autoritário e Analítico",
        "customer_label": "Cliente Jurídico",
        "core_service_label": "Processo Judicial",
        "critical_rules": ["Sigilo profissional absoluto"],
        "ai_persona": "Você é um Advogado Sênior e Negociador de Acordos."
    }
    with open("server/business_profile.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(profile_legal, f)
    
    res_legal = await negotiator.negotiate("5511888888888", objection, 5000.0)
    print(f"🤖 Resposta IA (Modo Jurídico):\n{res_legal}\n")

if __name__ == "__main__":
    # Ajustar path para rodar o teste
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    asyncio.run(test_agnostic_transmutation())

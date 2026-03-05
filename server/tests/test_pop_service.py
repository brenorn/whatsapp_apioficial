import asyncio
import os
import sys

# Ajustar path para incluir a pasta 'server'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compliance.pop_service import POPArchitectService

async def test_pop_elite():
    print("🧪 [TEST] Iniciando Teste de Geração de POP Elite (P18)...")
    
    service = POPArchitectService()
    
    # Simula um médico pedindo um POP de "Lavagem de Mãos em Ambiente Cirúrgico"
    topic = "Lavagem de Maos em Ambiente Cirurgico"
    phone = "5511999999999"
    
    print(f"🚀 [STEP 1] Gerando POP para: {topic}")
    response = await service.create_elite_pop(phone, topic)
    
    print("\n--- [ RESPOSTA PARA O WHATSAPP ] ---")
    print(response)
    print("------------------------------------\n")
    
    # Verifica se o arquivo foi criado
    filename = f"server/assets/pop_reports/POP_{topic.replace(' ', '_')}.md"
    if os.path.exists(filename):
        print(f"✅ [SUCCESS] Arquivo Markdown gerado em: {filename}")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            print("\n--- [ CONTEÚDO DO POP (PRIMEIRAS 500 LINHAS) ] ---")
            print(content[:1000] + "...")
    else:
        print(f"❌ [ERROR] Falha ao gerar o arquivo físico: {filename}")

if __name__ == "__main__":
    asyncio.run(test_pop_elite())

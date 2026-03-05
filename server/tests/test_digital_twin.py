import asyncio
import os
import sys

# Ajustar path para incluir a pasta 'server'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.digital_twin_service import DigitalTwinService

async def test_digital_twin_flow():
    print("🎙️ [TEST] Iniciando Fluxo do Gêmeo Digital (Voz Clonada - P16)...")
    
    twin = DigitalTwinService()
    
    # Simula um Doutor precisando enviar um briefing de exame de voz em 10 segundos 
    context = "O paciente 'João' perguntou se o exame de sangue dele acusou pré-diabetes pois a glicose deu 105. Diga que não precisa pânico, mas marcaremos retorno para ajustar a dieta."
    
    print("\n🧠 1. Gerando o roteiro do áudio (Text-to-Speech LLM)...")
    
    # Chama o Twin que usa a Factory no modo Sênior (Character Acting) e logo depois dispara a ElevenLabs
    audio_path, generated_text = await twin.talk_as_doctor("João", context)
    
    print("\n📝 [ROTEIRO GERADO]:")
    print(generated_text)
    
    print("\n🔊 [CAMINHO DO AUDIO MP3]:")
    if audio_path:
        print(f"✅ Arquivo estaria em: {audio_path}")
    else:
        print("⚠️ Caminho nulo (API Key da ElevenLabs ausente ou falha na rede, o que é esperado no teste mockado).")

if __name__ == "__main__":
    asyncio.run(test_digital_twin_flow())

import os
import sys
from dotenv import load_dotenv

# ============== 1. CARREGAMENTO INICIAL ==============
# Garante que as variáveis de ambiente (Tokens, Portas, Senhas de Banco)
# sejam carregadas antes de qualquer outra biblioteca do projeto.
load_dotenv()

# ============== 2. FIX DE IMPORTAÇÕES UNIVERSAIS ==============
# Define o diretório atual (onde o main.py está) como a raiz do Python.
# Isso permite que 'from api.webhook_server import app' funcione em
# qualquer computador (Windows, Linux, Docker, etc) sem quebrar.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ============== 3. INICIALIZAÇÃO DA APLICAÇÃO ==============
try:
    from api.webhook_server import app
except ImportError as e:
    print(f"❌ Erro Crítico: Falha ao importar a API. Verifique a estrutura das pastas. Detalhe: {e}")
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    # Pega a porta do .env (Se não existir, usa a 5005)
    port = int(os.getenv("PORT_WEBHOOK", 5005))
    
    print("=" * 60)
    print("🚀 FASTAPI STARTED: WhatsApp Cloud API Oficial")
    print("🛡️  Modo Blindado: ASYNC BACKGROUD TASKS + ZERO TRUST")
    print(f"🌐 Porta do Webhook: {port}")
    print("=" * 60)
    
    # Inicia o servidor ASGI Uvicorn (Padrão de Prod para FastAPI)
    uvicorn.run("api.webhook_server:app", host="0.0.0.0", port=port, reload=False)

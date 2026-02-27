import os

base_path = r"D:\OneDrive\aiproj\0 move\whatsapp_apioficial"

structure = {
    "docs/ARCHITECTURE.md": "# Arquitetura\n\nMapa detalhado da arquitetura e fluxos do WhatsApp Oficial com Handoff Monitor.",
    "docs/HANDOFF_SYSTEM.md": "# Sistema de Handoff (Regra de Ouro)\n\nSe a última mensagem no banco foi enviada por `sender='me'`, a IA bloqueia e o humano assume o controle.",
    "server/.env": "META_VERIFY_TOKEN=movemind_secure_token\nMETA_API_TOKEN=seu_token_aqui\nDATABASE_URL=postgresql://user:pass@localhost:5432/whatsapp\nPORT=5005",
    "server/requirements.txt": "Flask==3.0.0\nrequests==2.31.0\npydantic==2.5.3\npython-dotenv==1.0.0\npsycopg2-binary==2.9.9",
    "server/api/webhook_server.py": '"""\nServidor Flask para Handshake da Meta API Oficial.\n"""\nfrom flask import Flask, request, jsonify\nimport os\n\napp = Flask(__name__)\n\n@app.route("/webhook/meta", methods=["GET", "POST"])\ndef webhook_meta():\n    pass\n\nif __name__ == "__main__":\n    app.run(port=int(os.getenv("PORT", 5005)))',
    "server/api/schemas.py": "# Pydantic models para validacao dos payloads da Meta",
    "server/core/orchestrator.py": "# Coordena o recebimento, verifica Handoff e chama IA",
    "server/core/whatsapp_cloud_client.py": "# Cliente HTTP para envio de mensagens via Meta Cloud API",
    "server/core/webhook_parser.py": "# Analisador de payloads complexos da Meta API",
    "server/ai/main_brain.py": "# Cerebro principal de decisao IA",
    "server/ai/intent_analyzer.py": "# Classificador de intencoes (ex: cancelamento vs reagendamento)",
    "server/ai/memory_manager.py": "# Recuperacao de ultimas mensagens do usuario",
    "server/database/connection.py": "# Pool de conexao PostgreSQL",
    "server/database/repository.py": "# Funcoes utilitarias de CRUD no banco (checagem de Handoff)",
    
    "chat_monitor/backend/package.json": '{\n  "name": "chat-monitor-backend",\n  "version": "1.0.0",\n  "main": "server.js",\n  "dependencies": {\n    "express": "^4.18.2",\n    "socket.io": "^4.7.4",\n    "pg": "^8.11.3",\n    "cors": "^2.8.5",\n    "dotenv": "^16.4.5"\n  }\n}',
    "chat_monitor/backend/server.js": "// Backend Node.js (Porta 5006) com Express e Socket.io",
    "chat_monitor/backend/chat_controller.js": "// Controladores de historicos de conversas e envios manuais do monitor",
    "chat_monitor/backend/db.js": "// Conexao rapida com PostgreSQL (node-postgres)",
    
    "chat_monitor/frontend/package.json": '{\n  "name": "chat-monitor-frontend",\n  "version": "1.0.0",\n  "scripts": {\n    "dev": "vite",\n    "build": "vite build"\n  },\n  "dependencies": {\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0",\n    "socket.io-client": "^4.7.4"\n  },\n  "devDependencies": {\n    "vite": "^5.1.0"\n  }\n}',
    "chat_monitor/frontend/vite.config.js": 'import { defineConfig } from "vite";\nimport react from "@vitejs/plugin-react";\n\nexport default defineConfig({\n  plugins: [react()],\n  server: {\n    port: 5173\n  }\n});',
    "chat_monitor/frontend/src/App.jsx": "// SPA App principal do React",
    "chat_monitor/frontend/src/ChatWindow.jsx": "// Componente de interface de mensagens (cores de bolhas: cliente vs IA vs humano)",
    "chat_monitor/frontend/src/socket.js": "// Configuracao do cliente socket.io",
    
    "scripts/init_db.sql": "-- DDL Schema\nCREATE TABLE IF NOT EXISTS whatsapp_messages (\n    id SERIAL PRIMARY KEY,\n    phone VARCHAR(20) NOT NULL,\n    message TEXT NOT NULL,\n    sender VARCHAR(10) NOT NULL CHECK (sender IN ('user', 'bot', 'me')),\n    message_type VARCHAR(20) DEFAULT 'text',\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);",
    "scripts/start_tunnel.ps1": '# Inicia o tunnel (ex: cloudflared)\nWrite-Host "Iniciando Tunnel..."\n# cloudflared tunnel --url http://localhost:5005'
}

for rel_path, content in structure.items():
    full_path = os.path.join(base_path, rel_path.replace("/", "\\"))
    full_dir = os.path.dirname(full_path)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
        
print("Estrutura criada com sucesso!")

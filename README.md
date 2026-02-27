# 🚀 WhatsApp Official Boilerplate (Design Partner BMAD)

Este projeto soluciona os problemas de escala encontrados no legado do projeto Move (`cerebro.py`). Ele desmembra o que era um monolito gigante em microsserviços blindados e super velozes.

## 🌟 O que Difere do Antigo Move_Git?

### 1. 🧹 Morte do Monólito
No `move_git`, o arquivo `cerebro.py` de quase 600 linhas absorvia responsabilidades demais:
- Lidava com a rede HTTP da Meta.
- Lidava com o RAG/LangChain.
- Servia HTMLs na força bruta e carregava até o bundle Vite do React na `/painel`.

**A Evolução Aqui:** 
Desmembramos. O arquivo `server/api/webhook_server.py` só fala HTTP e tem 40 linhas. A extração de Lógica de rede foi para `core/webhook_parser.py` para nunca mais lermos Dict Keys complexas misturadas com código de Prompts de IA. O FrontEnd React vive e roda num container estático NPM separado.

### 2. 🛡️ O "Handoff Real" (A Regra de Ouro)
Antigamente, se o Chat Monitor NodeJS engasgasse ou travasse, a IA ignorava o clique do humano de `Pausar` (via requisição http do Python -> Node) e voltava a responder o Lead em paralelo.
**A Evolução Aqui:** Implementamos o Handoff pela Base de Dados (Database First). Se o Analista mandou um 'Oi!', o NodeJS posta isso no PostgreSQL como `sender='me'`. Na próxima API Call o Orquestrador varre essa linha e a IA nunca mais responde até ser liberada, não importa se o Monitor esteja rodando off.

---

## 🏎️ Como Começar Agora? (Universal Run)

O projeto foi cabeado e montado para rodar através do único entrypoint Universal (Agnóstico a Paths do Windows ou Docker):

**Subir a Casca e IA (Python 3.10+)**
```bash
cd server
pip install -r requirements.txt
cp ../.env.example ../.env
python main.py
```
*A porta subirá em 5005, já esperando o Cloudflared.*

**Subir o Monitor Visual (Node.JS)**
```bash
# Terminal 2 - Back (Motor Rápido de DB)
cd chat_monitor/backend
npm install
npm run start 

# Terminal 3 - Front VITE (O Painel do Atendente)
cd chat_monitor/frontend
npm install
npm run dev
```

---
**Criado por:** Antigravity AI Design Pattern Architect  
**Princípios:** S.O.L.I.D. | BMAD | Micro-serviços

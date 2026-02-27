# 🚀 Projeto Base: Integração WhatsApp API Oficial + Chat Monitor

Este documento detalha a arquitetura, estrutura de diretórios, nomenclatura de arquivos e as justificativas para a criação de um modelo de serviço duplicável, voltado para integração com a Meta Cloud API (WhatsApp Oficial) e um Sistema de Monitoramento com Handoff Automático (Chat Monitor), inspirado no ecossistema BMAD e na estabilidade testada do projeto `ClinicaMind/agentes_busca_dinamica`.

Este modelo foi desenhado como um Padrão de Design (Design Pattern) em equipe com especialistas seniores, visando máxima modularidade (S.O.L.I.D) e um domínio isolado.

---

## 🏗️ 1. Arquitetura Geral do Sistema (O Fluxo de Valor)

A arquitetura resolve o maior desafio de bots integrados com painéis humanos de atendimento (ChatMonitor/Chatwoot): o conflito de autoria das mensagens.

O fluxo adotado é chamado de **Handoff Reverso Baseado no Banco de Dados**:
1. **Webhook (Entrada):** O servidor HTTP (API) recebe a notificação da Meta.
2. **Parser e Identificação:** Os dados brutos da Meta são extraídos e traduzidos apenas para `(phone, message_text)`.
3. **Verificação de Handoff (A Regra de Ouro):** O Orquestrador verifica no banco de dados quem mandou a última resposta para aquele telefone. Se a última mensagem enviada foi classificada como `sender='me'` (Humano via ChatMonitor), a **IA é automaticamente travada** e o webhook não prossegue para processamento.
4. **Cérebro (Brain / IA):** Se a IA estiver livre (última mensagem for `bot` ou não existir), o Brain gera e retorna a resposta via LLM baseada nas intenções do usuário.
5. **Meta Client (Saída):** A resposta da IA é disparada para a Meta via API HTTP Oficial e o fluxo é logado no banco como `sender='bot'`.
6. **Chat Monitor (Real-time):** Um backend Node.js com Socket.io e frontend React que escuta o banco de dados. Permite a um operador visualizar as mensagens, pausar proativamente a IA ou enviar uma mensagem como humano. Ao enviar pelo Monitor, a mensagem passa pelo Node.js, é disparada pela Meta, é salva com `sender='me'`, disparando a "Regra de Ouro" que bloqueará a IA nas requisições seguintes.

---

## 📂 2. Estrutura de Pastas e Arquivos

Esta estrutura padrão pode ser clonada como base (Boilerplate) para qualquer novo bot oficial.

```text
/whatsapp_oficial_base
│
├── 📁 docs/                             # Documentação contextual e especificações
│   ├── ARCHITECTURE.md                  # Mapa detalhado da arquitetura e fluxos
│   └── HANDOFF_SYSTEM.md                # Explicação clara da "Regra de Ouro" e estados
│
├── 📁 server/                           # (Python) Microsserviço de Webhook e Orquestração
│   ├── .env                             # Tokens (Meta, Banco, chaves da IA)
│   ├── requirements.txt
│   ├── 📁 api/
│   │   ├── webhook_server.py            # Servidor Flask ou FastAPI para o handshake da Meta
│   │   └── schemas.py                   # Validação de dados (Pydantic models)
│   ├── 📁 core/
│   │   ├── orchestrator.py              # Coordena o recebimento, verifica Handoff e chama IA
│   │   ├── whatsapp_cloud_client.py     # Cliente HTTP (Requests) para disparos na Meta API API Oficial
│   │   └── webhook_parser.py            # Analisador robusto de payloads (extrai textos e áudios do JSON da Meta)
│   ├── 📁 ai/
│   │   ├── main_brain.py                # LangChain ou roteador manual de LLM
│   │   ├── intent_analyzer.py           # Classifica a intenção do texto antes de gerar texto grande
│   │   └── memory_manager.py            # Busca n mensagens anteriores da conversa
│   └── 📁 database/
│       ├── connection.py                # Pool de conexão PostgreSQL (onde os chats ficam armazenados)
│       └── repository.py                # Funções de INSERT/SELECT fáceis (logs de chat, checagem da última mensagem)
│
├── 📁 chat_monitor/                     # (Node.js) Microsserviço Administrativo e de Handoff
│   ├── 📁 backend/
│   │   ├── package.json
│   │   ├── server.js                    # Express API (Porta 5006) + Socket.io para envio de alertas
│   │   ├── chat_controller.js           # Funções que puxam mensagens, enviam como humano e geram socket broadcast
│   │   └── db.js                        # Comunicação rápida com PostgreSQL via node-postgres
│   └── 📁 frontend/
│       ├── package.json
│       ├── vite.config.js
│       ├── 📁 src/
│       │   ├── App.jsx                  # Single Page Application principal (React)
│       │   ├── ChatWindow.jsx           # Componente que mostra a conversa e tem bolhas de cores (Me vs Bot)
│       │   └── socket.js                # Cliente de gerenciamento de conexão Websocket
│
└── 📁 scripts/                          # Helpers Operacionais
    ├── init_db.sql                      # DDL do esquema (whatsapp_messages, handoff_states)
    └── start_tunnel.sh                  # Inicia o cloudflared / ngrok para testar Webhook da Meta
```

---

## 📝 3. Nomenclatura dos Arquivos e Justificativas Técnicas

### No Núcleo do Webhook (Python)

*   **`api/webhook_server.py`**
    *   **Função:** Ponto de entrada. Um arquivo limpo que lida puramente com a internet. Terá a rota `GET /webhook/meta` (Handshake Verify Token) e `POST /webhook/meta` (Payload Parser).
    *   **Justificativa:** Separar a casca HTTP da regra de negócio evita que exceções de parse quebrem a integridade da comunicação.

*   **`core/webhook_parser.py`**
    *   **Função:** A Meta tem payloads JSON extremamente complexos e com chaves embutidas. Este arquivo só filtra isso.
    *   **Justificativa:** Mantém a sujeira da Meta fora do orquestrador principal. Garante que qualquer troca na API Cloud seja absorvida apenas aqui.

*   **`core/orchestrator.py`**
    *   **Função:** Gerente do pedaço. Pega a mensagem, pergunta ao repositório o "status do Handoff" (Regra de Ouro), decide se descarta a mensagem silenciosamente (Humano assumiu) ou encaminha para `main_brain.py`.
    *   **Justificativa:** É a cola entre a IA e o "chat com a Meta". Em sistemas multicamadas, o orquestrador é fundamental para manter o SRP (Single Responsibility Principle).

*   **`core/whatsapp_cloud_client.py`**
    *   **Função:** Arquivo que tem as classes para efetuar HTTP POST para `graph.facebook.com/v21.0/PHONE_ID/messages`. Centraliza requisições HTTP Bearer.
    *   **Justificativa:** Facilita mocks em testes e retentativas locais (retries), isolando tokens e URLs.

### No Chat Monitor (Node/React)

*   **`chat_monitor/backend/server.js`**
    *   **Função:** Sobe Express + Socket.IO. Provê `/api/chats` para listar e escuta emissões no envio de mensagens humanas.
    *   **Justificativa:** O real-time usando Node (Socket.io) é universal e leve (comparado ao WebSocket nativo em Python). Permite separar painéis de relatórios dos servidores brutamontes de linguagem Python.

*   **`chat_monitor/frontend/ChatWindow.jsx`**
    *   **Função:** UI para atendimento. As mensagens tem coloração baseada no remetente (`bot`: azul da IA, `user`: cinza cliente, `me`: verde operador humano).
    *   **Justificativa:** Permite que a equipe de operação compreenda intuitivamente que o controle está com eles e não mais com o robô. Ter um componente separado focado em re-renderização agrada a performance.

*   **`scripts/init_db.sql`**
    *   **Função:** Contém o schema de `whatsapp_messages` (`phone`, `message`, `sender`, `created_at`).
    *   **Justificativa:** A "Regra de Ouro" depende explicitamente do log ordenado por data e do metadado "sender". Um banco de dados bem montado desde o dia zero (o que não tem no SQLite padrão) salva o fluxo de Handoff automático.

---

## 🔒 4. O Sistema de Handoff ("A Regra de Ouro")

O maior diferencial desta arquitetura é o bloqueio automático de intrusão, operado da seguinte maneira. O banco de dados do projeto, mais especificamente a tabela base, deverá ter uma coluna crucial: `sender` (remetente).
`sender` aceita os valores enum: `bot`, `user`, `me`.

1. **Atendente assume o controle:** O atendente humano abre a tela do Frontend, escreve uma mensagem para socorrer um cliente mal atendido e aperta Enviar. O Backend em NodeJS chama a Meta API, a mensagem de socorro é enviada ao cliente e esse evento no sistema inteiro fica marcado com um Log no Banco com a Flag `sender='me'`.
2. **Cliente responde ao humano:** Em decorrência do socorro, o cliente no WhatsApp envia: "Obrigado! Consegue aprovar o projeto?".
3. **Webhook da Meta:** O payload chega no servidor Python de Webhook e é repassado para o orquestrador (`orchestrator.py`).
4. **Proteção de Intrusão IA:** O `orchestrator.py` executa o SQL `SELECT sender FROM whatsapp_messages WHERE phone = 'XXXX' AND sender != 'user' ORDER BY created DESC LIMIT 1`. A query retorna `me` (a última mensagem lançada com sucesso do lado corporativo foi de um ser humano da equipe).
5. **Decisão:** A Inteligência Artificial (Brain) e LLMs não devem ser instanciadas nem invocadas em momento algum, não se gasta processamento e a resposta é finalizada com OK na Meta ("não enviamos as mensagens de máquina"). O FrontEnd Socket.IO no ChatMonitor mostra a segunda mensagem nova do cliente. O Humano que assumiu ainda está na máquina para respondê-la, completando a interação humana.

Se e quando o humano desejar voltar a IA ao normal, pode apertar o botão [Reativar Inteligência IA] -> que posta uma mensagem invisível simulada, inserindo forçadamente uma linha no banco com `sender='bot'` de forma a falsear a query acima nas próximas vezes e a IA volta a operar naturalmente.

---

## 💡 5. Conclusão para Duplicação (Checklist de Deploy)

Ao utilizar esta arquitetura, independente se a demanda for "Bot de Vendas de Cursos" ou "Agent de Recuperação de Carrinho", o desenvolvedor precisará apenas:

1. **Clonar esta estrutura** em uma nova branch ou repo.
2. **Substituir Prompts e Logicas** apenas na pasta `ai/main_brain.py` (Deixar Webhook, Meta, e Parsing intactos).
3. **Gerar tokens da Meta Apps** e adicionar no seu `.env`.
4. **Subir a interface do Chat Monitor** (`npm run dev`) e expor as rotas via firewall.
5. Em menos de 10 minutos, haverá um serviço WhatsApp totalmente blindado, oficial e com interface Real-Time e handoffs.

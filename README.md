<div align="center">
  <h1>🧠 Ecossistema MoveMind 360: Plataforma SaaS de IA Agnóstica (V3.0)</h1>
  <p><b>Inteligência Artificial Universal, Adaptável a Qualquer Setor.</b></p>
  <p>Um orquestrador Omni-Direcional com 25 Microserviços de IA para Clínicas, Escritórios de Advocacia, Imobiliárias e Negócios de Alta Performance.</p>
</div>

---

## ⚖️ O Manifesto: "IA com Alma, Corpo de Aço"
Nosso sistema não é apenas um "chatbot". É um ecossistema de microserviços projetado com uma filosofia estrita de engenharia que equilibra o brilho da Inteligência Artificial com a segurança brutal do código puro:

1. **SaaS Agnóstico (Nova Camada):** O sistema troca de "pele" instantaneamente via arquivo `business_profile.yaml`. Mesma IA, setores diferentes (Advocacia, Saúde, Vendas).
2. **HybridRAG Engine (Cérebro Cognitivo):** Integração mestre entre **PostgreSQL** (Fatos), **Neo4j** (Relações/GraphRAG) e **ChromaDB** (Vetores). O sistema não apenas responde, ele raciocina sobre conexões complexas.
3. **Knowledge Vault (Sandeco Master Architecture):** Pipeline profissional de ingestão (Chunking -> Extraction -> Aggregation). Alimente a IA com livros e artigos e veja-a aprender em Domínios isolados (Area X).
4. **Escudo de Segurança (Corpo de Aço):** Código determinístico para tarefas críticas. Custo zero, latência zero, 100% de precisão.

---

## 🚀 Os 25 Projetos / Microserviços Integrados
Este repositório consolida 25 projetos modulares em um único cérebro centralizado, divididos em categorias estratégicas:

### 💼 Vendas e Commerce
*   **01. Payment Gateway:** Checkout e faturamento via PIX automático no próprio chat WhatsApp.
*   **10. NPS 3.0:** Jornada inteligente de encantamento e pesquisa de satisfação humanizada.
*   **19. Sales Negotiator:** Agente treinado com táticas do FBI (Chris Voss) para contornar objeções de preço.
*   **20. Loyalty Program:** Gamificação, XP e níveis de retenção de clientes VIP.
*   **25. AI Outreach:** O "Drone". Prospecção ativa humana baseada em mineração de dados esquecidos.

### 🧠 Inteligência & Governança Clínica
*   **08. CEO BI Dashboard:** Execução e leitura de banco de dados via linguagem natural.
*   **17. Meeting Intel:** Geração rápida de Atas e Mapas Mentais (código Mermaid) pós-consulta.
*   **18. POP Architect:** Criação modular de Procedimentos Operacionais Padrão (Metodologia 5W2H) integrados ao Miro.
*   **21. BI 360 Executivo:** Análise preditiva e geração de *Flash Reports* automáticos.
*   **22. Health Vault:** Prontuário impulsionado por MedGemma com sistema RAG imune a alucinações.

### 📢 Marketing & Audiência (Growth)
*   **06. Social Command:** Gestão centralizada para criação de carrosséis narrativos.
*   **07. Strategic Growth:** Acompanhamento de tendências do Google Trends.
*   **12. Omni Social Hub:** Distribuidor unificado de conteúdo para Instagram, TikTok e LinkedIn.
*   **13. Google Ads Engine:** IA analisadora de tráfego, ROI e campanhas do Adwords pelo chat.
*   **14. SEO Machine:** Redator técnico E-E-A-T que publica organicamente em blogs WordPress.
*   **15. Video Auto-Editor:** Serviço de cortes mágicos (*Silence Sniper*) e legendagem dinâmica estilo Alex Hormozi.

### 🛡️ Compliance, Experiência e Omni-Channel
*   **02. STT Audio:** Transcrição veloz de áudios longos do paciente injetados no contexto da IA.
*   **03. Flows Manager:** Controle visual e formulários dinâmicos da interface da Meta.
*   **04. CAPI Tracker:** API de Conversões para atribuição perfeita de cada R$ investido.
*   **05. Broadcast Engine:** Motor de disparos ativos em massa (HSM).
*   **09. Escudo NR-01:** Módulo de segurança, saúde mental corporativa e auditoria psicossocial.
*   **11. Group Intel:** Sistema Sentinel para moderação automática e Scout de Leads em grupos de WhatsApp.
*   **16. Digital Twin (Voz):** Clonagem de voz do médico via ElevenLabs para respostas em áudio extremamente reais.
*   **23. Streaming Live:** Gêmeo digital interativo para vídeo.
*   **24. Command Flows:** Mini-aplicativos nativos no WhatsApp para gestão operacional.

---

## 🏗️ Arquitetura Sênior

A arquitetura do projeto foi desenhada para não travar o **FastAPI** e evitar "Código Espaguete". 
Regra interna: **Nenhum arquivo de negócio deve passar das 200 linhas.**

*   `server/core/orchestrator.py`: O coração do tráfego. Recebe a mensagem e delega.
*   `server/core/interceptors_manager.py`: Os 25 projetos ficam aqui. Se a intenção for do Projeto 15, ele isola e despacha.
*   `server/core/guardrails_manager.py`: A alfândega. Filtra palavrões, links maliciosos e anonimiza CPFs/E-mails (Zero Leak).
*   `server/core/config_manager.py`: O "DNA" do setor. Controla a troca de contexto entre Clínica/Advocacia.
*   `server/ai/knowledge_vault/`: Motor de ingestão GraphRAG (Inspirado no Sandeco). Onde livros e artigos viram inteligência estruturada.
*   `server/ai/rag_manager.py`: Orquestrador Híbrido que funde Graph + SQL + Vector em uma única resposta contextual.
*   `server/ai/llm_factory.py`: Fábrica de LLMs com fallback automático e injeção de contexto agnóstico.
*   `docker-compose.yml`: Orquestração profissional (FastAPI + PostgreSQL + Neo4j).

---

## ⚙️ Instalação e Start Rápido

### Pré-Requisitos
*   Python 3.10+
*   PostgreSQL
*   Acesso aos tokens da Google Cloud, Meta (WhatsApp Cloud API) e demais provedores (Miro, WP, etc).

### Passo a Passo

**1. Clone o ambiente e crie o arquivo virtual:**
```bash
python -m venv .venv
source .venv/Scripts/activate # Windows
# ou source .venv/bin/activate # Linux/Mac
```

**2. Instale o "Motor":**
```bash
pip install -r requirements.txt
```

**3. Configure o Cérebro:**
Copie o template de ambiente e o atualize com suas chaves.
```bash
copy .env.example .env
```
*(Preencha as chaves: `GEMINI_API_KEY`, `WHATSAPP_TOKEN`, conexão com o Bando de Dados, etc).*

**4. Dê vida ao ecossistema:**
```bash
python server/main.py
```
> O servidor rodará na porta `8000` (ou a definida no .env). Se configurado corretamente, o webhook da Meta começará a injetar as mensagens neste endpoint.

---

## 🛡️ Camada Guardrails: A Biblioteca de Blindagem
Localizada dentro da engenharia do server, temos os validadores analíticos que bloqueiam o imprevisível:
- **Jailbreak Detection:** A IA nunca obedece clientes que tentam reconfigurá-la.
- **SQL Predicates Check:** Se a IA for gerar um relatório, o Guardrail bloqueia `DROP`, `DELETE` ou `TRUNCATE`.
- **Competitor Check:** A IA se recusa a comentar sobre clínicas concorrentes específicas.
- *(Consulte `projetos/GUARDRAILS_CENTRAL.md` para ver as 15+ regras de segurança adicionais).*

---
<div align="center">
  <i>Construído para escalar faturamento preservando a marca, a ética médica e a saúde mental dos colaboradores.</i>
</div>

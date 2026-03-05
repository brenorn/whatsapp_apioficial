# 🛠️ PENDÊNCIAS MESTRE: MOVEMIND 360 (v1.0)
> **Status:** Mapeamento de Transição para Plataforma SaaS Agnóstica.

Este documento consolida as pendências técnicas de todos os microserviços, priorizando a unificação no **Docker** e no **Multi-Setor**.

---

## 🏗️ INFRAESTRUTURA & CORE
- [x] **Agnostic Core:** `BusinessConfigManager` implementado e integrado à LLMFactory (Transmutação funcional).
- [ ] **Docker Engine:** Validar a conexão real entre o container de Backend e o Postgres/Neo4j via `docker-compose up`.
- [ ] **Neo4j Seeder:** Implementar o script que popula o Grafo inicial de conhecimento (Injetar Nós de Setores).
- [ ] **Environment Audit:** Centralizar todas as chaves (ElevenLabs, Meta, Google, Miro) no `server/.env`.

---

## 📈 MARKETING & GROWTH (P13, P14, P15)
- [ ] **Omni-Ads SDKs:** Substituir os motores mocked em `meta_engine.py` e `google_engine.py` pelas chamadas reais das APIs (facebook-business e google-ads).
- [ ] **Hormozi Editor (P15):** Integrar o `Whisper` (OpenAI ou Local) para que as legendas automáticas sejam 100% reais e sincronizadas.
- [ ] **WP SEO Publish:** Finalizar a conexão com a API do WordPress para postagem automática de artigos gerados pela IA.

---

## 🏥 CLÍNICA & JURÍDICO (P22, P17, P18)
- [ ] **Health Vault RAG:** Conectar o `HealthVaultEngine` aos arquivos `.md` históricos do `knowledge_base` via Neo4j.
- [ ] **Meeting Intel Map:** Garantir que o código Mermaid gerado apareça formatado corretamente na tela do dashboard ou via link.
- [ ] **POP Mirror:** Automatizar a criação do quadro no Miro diretamente após a geração do POP pelo WhatsApp.

---

## 🤝 VENDAS & COMMERCE (P1, P19, P20)
- [ ] **Payment PIX Webhook:** Desenvolver o endpoint de recebimento de notificações do Banco (Baas) para atualizar o status de `PENDING` para `PAID` automaticamente.
- [ ] **Loyalty Ranking:** Integrar o sistema de XP com o histórico de transações reais do `MASTER_DATABASE_SCHEMA`.
- [ ] **Negotiator A/B:** Refinar os prompts de negociação dinâmica baseada no `SETOR` atual do `BusinessConfig`.

---

## 📊 EXECUTIVO & BI (P8)
- [ ] **Master BI Orchestrator:** Desenvolver a IA capaz de ler "Selects" no Banco Master sob demanda humana (O cérebro financeiro do sistema).
- [ ] **Flash Report Scheduler:** Criar o Cron Job que envia um resumo do dia para o dono da empresa às 18:00 todos os dias.

---

## 🛡️ COMPLIANCE & SEGURANÇA (GUARDRAILS)
- [ ] **Hallucination Judge:** Implementar o validador que checa se a resposta da IA contradiz o banco de dados Master antes de enviar ao cliente.
- [ ] **PII Scrubbing:** Expandir o validador para detectar documentos específicos (OAB/CRM) e anonimizá-los conforme LGPD.

---

## 🛰️ CONECTIVIDADE & FUTURO (P26)
- [ ] **Project 26 (MCP Global Gateway):** Implementar o Model Context Protocol para conectar o MoveMind aos dados nativos do Google Workspace e BigQuery do cliente de forma agnóstica.

---
*Assinado: Antigravity AI Engine (Breno's Co-Pilot)*

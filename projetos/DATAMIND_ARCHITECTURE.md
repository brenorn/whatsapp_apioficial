# 🗄️ ARQUITETURA DE DADOS: MOVEMIND 360
> **Conceito:** Estrutura unificada de Domínios para os 25 Microserviços de IA.

Este documento explica como o Banco de Dados Mestre sustenta a inteligência do ecossistema, utilizando uma abordagem híbrida de **PostgreSQL (Memória Transacional)** e **Neo4j (Intuição e Conexão)**.

---

## 🔝 1. Visão Geral da Modelagem
Em vez de criar uma tabela para cada serviço, o MoveMind 360 utiliza **Domínios de Dados**. Isso permite que o **Módulo CEO BI (P8)** realize cruzamentos complexos (ex: Correlacionar ROAS de Ads com Nível de Fidelidade do Cliente) de forma instantânea.

---

## 🐘 2. PostgreSQL: O Corpo Transacional
Localização do Script: `scripts/MASTER_DATABASE_SCHEMA.sql`

### 🏗️ Grupos de Tabelas vs. Projetos

#### 📩 A: Núcleo de Mensageria (Handoff & Log)
*   **Tabela:** `whatsapp_messages`
*   **Projetos:** Atende a **Todos (P1-P25)**.
*   **Finalidade:** Log absoluto de interações, controle de fluxo e Handoff para humanos.

#### 🤝 B: Commerce & Negociação (Profit Center)
*   **Tabelas:** `negotiation_logs`, `hot_leads`
*   **Projetos:** P19 (Negotiator), P1 (Payments), P25 (Outreach).
*   **Finalidade:** Registrar objeções contornadas e conversões de alto ticket.

#### 📈 C: Inteligência de Negócio (BI & Marketing)
*   **Tabelas:** `ads_performance`, `bi_events`, `nps_responses`
*   **Projetos:** P13 (OmniAds), P8 (CEO BI), P10 (NPS).
*   **Finalidade:** Dashboards em tempo real e análise de sentimento do cliente.

#### 🏥 D: Intelligence Vault (Conhecimento)
*   **Tabelas:** `medical_vault`, `medical_logs`, `meeting_insights`, `pop_logs`
*   **Projetos:** P22 (Health Vault), P17 (Meeting Intel), P18 (POP Architect).
*   **Finalidade:** Armazenar transcrições, resumos clínicos e históricos de auditoria.

#### 🎞️ E: Assets Digitais (Clonagem & Vídeo)
*   **Tabela:** `digital_assets`
*   **Projetos:** P16 (Digital Twin), P15 (Video Editor/Hormozi).
*   **Finalidade:** Referenciar caminhos de arquivos de áudio clonados e vídeos processados.

---

## 🕸️ 3. Neo4j: O Cérebro de Grafos (Intuição)
Enquanto o Postgres guarda os fatos, o **Neo4j** guarda as **Relações**.

| Tipo de Nó | Relação | Objetivo |
| :--- | :--- | :--- |
| **Sintoma** | `RELACIONADO_A` | Suporte a diagnóstico clínico (P22). |
| **Cláusula** | `CONTRADIZ` | Auditoria jurídica automática (P17). |
| **Campanha** | `ALIMENTA_LEAD` | Atribuição multi-toque para o BI (P8). |

---

## 🛸 4. Escalabilidade & Agnosticismo
Gracias ao uso de **JSONB** no Postgres, as tabelas podem armazenar metadados diferentes dependendo do setor definido no `business_profile.yaml`:
*   No setor **Médico**, a tabela `nps_responses` armazena "Satisfação com o Procedimento".
*   No setor **Jurídico**, a mesma tabela armazena "Segurança no Acordo".

---
<div align="center">
  <i>Documento gerado pela Engenharia de Dados MoveMind.</i>
</div>

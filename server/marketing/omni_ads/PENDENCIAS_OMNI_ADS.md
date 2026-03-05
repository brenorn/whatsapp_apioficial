# 🎯 Omni-Ads: Arquitetura e Plano de Ação (Tráfego 360º)

Este documento descreve a arquitetura completa e as pendências para a implantação do módulo Omni-Ads, transformando o sistema em um verdadeiro "Growth Hacker" guiado por IA.

---

## 🔐 1. Variáveis de Ambiente (.env) Exigidas
Todas as credenciais abaixo devem ser configuradas no arquivo `.env` principal. Atualmente, os motores usam variáveis "MOCK_*" por segurança.

### Google Ads
```env
GOOGLE_ADS_DEVELOPER_TOKEN="sua_chave_aqui"
GOOGLE_ADS_CLIENT_ID="sua_chave_aqui"
GOOGLE_ADS_CLIENT_SECRET="sua_chave_aqui"
GOOGLE_ADS_REFRESH_TOKEN="sua_chave_aqui"
GOOGLE_ADS_CUSTOMER_ID="sua_chave_aqui" # ID da conta de anúncios (ex: 123-456-7890)
```

### Meta Ads (Facebook & Instagram)
```env
META_ADS_ACCESS_TOKEN="sua_chave_aqui" # System User Token gerado no Business Manager
META_AD_ACCOUNT_ID="act_123456789"     # ID da conta de anúncios
```

### TikTok Ads
```env
TIKTOK_ACCESS_TOKEN="sua_chave_aqui"
TIKTOK_ADVERTISER_ID="sua_chave_aqui"
```

### LinkedIn Ads (Tráfego B2B)
```env
LINKEDIN_ACCESS_TOKEN="sua_chave_aqui"
LINKEDIN_AD_ACCOUNT_ID="urn:li:sponsoredAccount:123456"
```

---

## 🗄️ 2. Estrutura de Banco de Dados (Database)
Para armazenar o histórico de performance, cruzar dados com agendamentos reais e permitir análises preditivas pela IA, as seguintes tabelas devem ser criadas no PostgreSQL (Módulo Escudo de Dados 360):

1. **`ads_daily_performance`**: Armazena a foto diária do tráfego.
   - `id` (UUID, PK)
   - `platform` (VARCHAR: google, meta, tiktok, linkedin)
   - `campaign_id` (VARCHAR)
   - `campaign_name` (VARCHAR)
   - `spend` (DECIMAL)
   - `impressions` (INT)
   - `clicks` (INT)
   - `conversions` (INT)
   - `cpl` (DECIMAL) # Custo por Lead
   - `roas` (DECIMAL) # Retorno do Investimento
   - `date` (DATE)

2. **`ads_ai_interventions`**: Log de auditoria das ações (autônomas ou sugeridas) tomadas pela IA.
   - `id` (UUID, PK)
   - `platform` (VARCHAR)
   - `campaign_id` (VARCHAR)
   - `action_type` (VARCHAR: PAUSE, INCREASE_BUDGET, DECREASE_BUDGET)
   - `old_value` (VARCHAR)
   - `new_value` (VARCHAR)
   - `reasoning` (TEXT) # Justificativa da IA para a ação
   - `status` (VARCHAR: PENDING_APPROVAL, EXECUTED, REVERTED)
   - `timestamp` (TIMESTAMP)

---

## 🧠 3. Motores, Backend e Agentes de IA

### A) Os Motores de Extração (Backend)
É necessário desenvolver os conectores reais substituindo os mocks nos seguintes arquivos (`server/marketing/omni_ads/`):
- [ ] **`google_engine.py`**: Desenvolver consultas GAQL (Google Ads Query Language) focadas em Search e Performance Max.
- [ ] **`meta_engine.py`**: Integrar a SDK `facebook_business` para leitura do *AdsInsights* e implementação da mutação (mudança de status da campanha).
- [ ] **`tiktok_engine.py`**: Implementar chamadas HTTP puro (httpx) para a TikTok Marketing API.
- [ ] **`linkedin_engine.py`**: Criar conector focado em métricas B2B corporativas.

### B) O Cérebro (Agente de IA - Growth Hacker)
- **`manager.py` (OmniAdsManager)**: 
  - Centraliza os dados de todas as APIs em paralelo (Async).
  - **Requisito Qualitativo:** A chamada da `LLMFactory` deve sempre exigir o nível **complex** (ex: Gemini 2.5 Pro), pois requer altíssimo Q.I. matemático e compreensão de lógica financeira. 
  - A IA cruzará as métricas com o funil interno (Agendamentos Feitos x Cliques na Plataforma) para descobrir se o lead gerado é "Lixo" ou "Qualificado".

---

## 🖥️ 4. Frontend e Interface (Human-in-the-Loop)

Embora o Whatsapp seja o canal de notificações ativas (Alertas Flash), o ecossistema requer visualização de controle:

1. **Dashboard do Gestor de Tráfego (Novo Módulo Web / B2B):**
   - **Visão Holográfica:** Gráficos cruzando Gastos das Plataformas Vs. Receita da Clínica.
   - **Intervention Center:** Uma tela onde o gestor visualiza todas as requisições pendentes da IA. Ex: *"A IA sugeriu pausar a campanha do Facebook. Aprovar [ ] Recusar [ ]"*.
   - Construir essa tela preferencialmente no ecossistema já existente (React / Next.js).

2. **WhatsApp Flows (Frontend Nativo no Chat):**
   - Criar um WhatsApp Flow para alterar orçamentos deslizando um dedo (Slider UI), permitindo que o CEO gerencie tráfego entre uma reunião e outra, sem precisar abrir o Gerenciador de Anúncios no computador.

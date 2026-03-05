-- =============================================================================
-- 🚀 MOVEMIND MASTER SCHEMA: UNIFICADO (v2.0)
-- Consolidação de todos os 25 Microserviços de IA
-- Escopo: PostgreSQL (Produção)
-- =============================================================================

-- 1. NÚCLEO DE MENSAGERIA E HANDOFF
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25) NOT NULL,
    message TEXT NOT NULL,
    sender VARCHAR(10) NOT NULL CHECK (sender IN ('user', 'bot', 'me')),
    message_type VARCHAR(20) DEFAULT 'text',
    message_status VARCHAR(20) DEFAULT 'delivered', -- sent, delivered, read, failed
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CRM & VENDAS (PROJETOS 1, 19, 25)
CREATE TABLE IF NOT EXISTS negotiation_logs (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25) NOT NULL,
    original_value NUMERIC(12,2),
    final_value NUMERIC(12,2),
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, WON, LOST
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hot_leads (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25) NOT NULL,
    source VARCHAR(50), -- Ex: Grupo_Networking, Ads_Meta
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. MARKETING E BI (PROJETOS 13, 10, 20)
CREATE TABLE IF NOT EXISTS ads_performance (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    stats JSONB, -- ROI, CPA, Cliques
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nps_responses (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25) NOT NULL,
    score INTEGER CHECK (score >= 0 AND score <= 10),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loyalty_accounts (
    phone VARCHAR(25) PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level VARCHAR(20) DEFAULT 'Bronze',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. GOVERNANÇA E INTELIGÊNCIA (PROJETOS 17, 18, 22)
CREATE TABLE IF NOT EXISTS medical_vault (
    phone VARCHAR(25) PRIMARY KEY,
    history_text TEXT, -- Prontuário RAG Transcrito
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medical_logs (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25),
    event VARCHAR(50), -- prescricao, alerta_alergia, consulta
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meeting_insights (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(25),
    content JSONB, -- Summary e Mermaid Code
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pop_logs (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    file_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. ATIVOS DIGITAIS (PROJETOS 15, 16)
CREATE TABLE IF NOT EXISTS digital_assets (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20), -- voice_clone, avatar_video, hormone_edit
    file_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. BI & EVENTOS GLOBAIS
CREATE TABLE IF NOT EXISTS bi_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ÍNDICES PARA ALTA PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_phone_messages ON whatsapp_messages(phone);
CREATE INDEX IF NOT EXISTS idx_nps_phone ON nps_responses(phone);
CREATE INDEX IF NOT EXISTS idx_medical_phone ON medical_vault(phone);

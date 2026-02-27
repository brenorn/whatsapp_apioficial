from database.connection import db_manager
import json

def is_ai_paused_for_phone(phone: str) -> bool:
    """Checa a Regra de Ouro (Quem foi o último a falar no Chat Monitor)."""
    conn = db_manager.connect()
    if not conn:
        return False  # Em modo MOCK (Sem .env), a IA nunca pausa.

    try:
        cur = conn.cursor()
        query = """
            SELECT sender FROM whatsapp_messages 
            WHERE phone = %s AND sender IN ('bot', 'me')
            ORDER BY created_at DESC LIMIT 1
        """
        cur.execute(query, (phone,))
        last_outbound = cur.fetchone()
        
        if last_outbound and last_outbound[0] == 'me':
            return True
        return False
    except Exception as e:
        print(f"❌ [DB ALERT] Falha ao checar Handoff para {phone}: {e}")
        return False

def log_message(phone: str, message: str, sender: str, msg_type: str = "text"):
    """Insere no Postgres a interacao para rastreio e Handoff"""
    conn = db_manager.connect()
    if not conn: return # MOCK MODE
        
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO whatsapp_messages (phone, message, sender, message_type, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (phone, message, sender, msg_type, json.dumps({})))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB ALERT] Erro logando a mensagem no banco: {e}")
        conn.rollback()

def update_message_status(wamid: str, phone: str, status: str):
    """
    Atualiza o Status (Read, Delivered, Failed) para espelhar Risquinhos Azuis 
    no Painel Node Front. Na V2 do DB deveremos anexar o wamid do disparo na row!
    """
    # Exemplo: Update whatsapp_messages set message_status = status where wamid = wamid
    # (Requer criar constraint de message_wamid na migration SQL futura)
    print(f"📬 [RECEIPT] {phone} marcou msg como '{status}'. (Wamid: {wamid})")

def execute_raw_bi_query(query: str) -> list:
    """
    [P8.3] Executa queries SQL dinâmicas (apenas leitura sugerida) 
    para o Módulo CEO Intelligence.
    """
    conn = db_manager.connect()
    if not conn: return []

    try:
        cur = conn.cursor()
        cur.execute(query)
        # Se for um SELECT, retorna os dados
        if cur.description:
            return cur.fetchall()
        conn.commit()
        return []
    except Exception as e:
        print(f"❌ [DB BI ALERT] Erro ao executar query dinâmica: {e}")
        conn.rollback()
        return []

# --- MÉTODOS PROJETO 9: NR-01 COMPLIANCE ---

def create_nr1_cycle(department: str, status: str = "OPEN") -> int:
    """Cria um novo ciclo de auditoria NR-01."""
    conn = db_manager.connect()
    if not conn: return 0
    try:
        cur = conn.cursor()
        query = "INSERT INTO nr1_cycles (department, status) VALUES (%s, %s) RETURNING id"
        cur.execute(query, (department, status))
        id = cur.fetchone()[0]
        conn.commit()
        return id
    except Exception as e:
        print(f"❌ [DB] Erro ao criar Ciclo NR1: {e}")
        return 0

def save_nr1_response(phone: str, data: dict):
    """Salva a resposta do colaborador para auditoria psicossocial."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO nr1_responses (phone, content, metadata) VALUES (%s, %s, %s)"
        cur.execute(query, (phone, json.dumps(data), json.dumps({})))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar resposta NR1: {e}")
        conn.rollback()

def get_nr1_stats(cycle_id: int) -> dict:
    """Retorna estatísticas sumárias de um ciclo específico."""
    # Placeholder para lógica de agregação futura
    return {"total_responses": 0, "burned_out_likely": 0}

# --- MÉTODOS PROJETO 10: NPS & REFERRAL ---

def save_nps_response(phone: str, score: int, feedback: str):
    """Salva a nota e o feedback do NPS."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO nps_responses (phone, score, feedback) VALUES (%s, %s, %s)"
        cur.execute(query, (phone, score, feedback))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar NPS: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 11: GROUP INTEL ---

def log_hot_lead(phone: str, source: str, context: str):
    """Registra uma demonstração de interesse vinda de um grupo."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO hot_leads (phone, source, context) VALUES (%s, %s, %s)"
        cur.execute(query, (phone, source, context))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao registrar Hot Lead: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 12: OMNICHANNEL SOCIAL ---

def log_social_post(platforms_data: dict, caption: str):
    """Registra o histórico de publicações em redes sociais."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO social_posts (platforms, caption) VALUES (%s, %s)"
        cur.execute(query, (json.dumps(platforms_data), caption))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao registrar post social: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 13: GOOGLE ADS ENGINE ---

def log_ads_performance(customer_id: str, data: dict):
    """Salva o resumo de performance diária do Google Ads."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO ads_performance (customer_id, stats) VALUES (%s, %s)"
        cur.execute(query, (customer_id, json.dumps(data)))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar performance Ads: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 14: SEO CONTENT MACHINE ---

def log_seo_article(title: str, wp_id: str):
    """Registra a criação e publicação de um artigo SEO."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO seo_logs (title, wordpress_id) VALUES (%s, %s)"
        cur.execute(query, (title, wp_id))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar artigo SEO: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 15: VIDEO AUTO-EDITOR ---

def log_video_edit(original_name: str, status: str):
    """Registra o processo de edição de um vídeo."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO video_logs (filename, status) VALUES (%s, %s)"
        cur.execute(query, (original_name, status))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar vídeo: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 16: DIGITAL TWIN & CLONING ---

def log_digital_asset(asset_type: str, path: str):
    """Registra a criação de um áudio ou vídeo clonado."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO digital_assets (type, file_path) VALUES (%s, %s)"
        cur.execute(query, (asset_type, path))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar ativo digital: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 17: MEETING INTEL ---

def log_meeting_insight(phone: str, data: dict):
    """Registra insights de reuniões e consultas."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO meeting_insights (phone, content) VALUES (%s, %s)"
        cur.execute(query, (phone, json.dumps(data)))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar insight: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 18: POP ARCHITECT ---

def log_pop_creation(topic: str, file_path: str):
    """Registra a criação de um documento POP."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO pop_logs (topic, file_path) VALUES (%s, %s)"
        cur.execute(query, (topic, file_path))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar POP: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 19: SALES NEGOTIATOR ---

def log_negotiation(phone: str, original_val: float, final_val: float, status: str):
    """Registra uma sessão de negociação e seu desfecho."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO negotiation_logs (phone, original_value, final_value, status) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (phone, original_val, final_val, status))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar negociação: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 20: LOYALTY PROGRAM ---

def get_loyalty_data(phone: str) -> dict:
    """Busca dados de gamificação do paciente."""
    conn = db_manager.connect()
    if not conn: return {"xp": 0, "level": "Bronze"}
    try:
        cur = conn.cursor()
        query = "SELECT xp, level FROM loyalty_accounts WHERE phone = %s"
        cur.execute(query, (phone,))
        row = cur.fetchone()
        return {"xp": row[0], "level": row[1]} if row else {"xp": 0, "level": "Bronze"}
    except Exception as e:
        print(f"❌ [DB] Erro ao buscar pontos: {e}")
        return {"xp": 0, "level": "Bronze"}

def update_loyalty_xp(phone: str, xp: int, level: str):
    """Atualiza o saldo de XP e o Nível."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO loyalty_accounts (phone, xp, level) VALUES (%s, %s, %s) ON CONFLICT (phone) DO UPDATE SET xp = %s, level = %s"
        cur.execute(query, (phone, xp, level, xp, level))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar pontos: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 22: HEALTH VAULT & MEDICAL ---

def get_medical_history(phone: str) -> str:
    """Busca o histórico médico bruto (PDFs transcritos ou notas)."""
    conn = db_manager.connect()
    if not conn: return "Sem histórico disponível."
    try:
        cur = conn.cursor()
        query = "SELECT history_text FROM medical_vault WHERE phone = %s"
        cur.execute(query, (phone,))
        row = cur.fetchone()
        return row[0] if row else "Nenhum prontuário encontrado."
    except Exception as e:
        print(f"❌ [DB] Erro ao buscar histórico: {e}")
        return "Erro ao acessar o Vault."

def log_medical_event(phone: str, event_type: str, data: dict):
    """Registra um evento clínico (alerta, consulta, prescrição)."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO medical_logs (phone, event, metadata) VALUES (%s, %s, %s)"
        cur.execute(query, (phone, event_type, json.dumps(data)))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar evento clínico: {e}")
        conn.rollback()

# --- MÉTODOS GERAIS: BI & EVENTOS ---

def log_bi_event(event_name: str, metadata: dict):
    """Registra um evento genérico para análise de BI (Projeto 21)."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO bi_events (event_name, metadata) VALUES (%s, %s)"
        cur.execute(query, (event_name, json.dumps(metadata)))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao logar evento BI: {e}")
        conn.rollback()

# --- MÉTODOS PROJETO 25: CONVERSATIONAL OUTREACH ---

def log_outreach(phone: str, campaign_type: str):
    """Registra uma tentativa de contato ativo."""
    conn = db_manager.connect()
    if not conn: return
    try:
        cur = conn.cursor()
        query = "INSERT INTO outreach_logs (phone, campaign) VALUES (%s, %s)"
        cur.execute(query, (phone, campaign_type))
        conn.commit()
    except Exception as e:
        print(f"❌ [DB] Erro ao registrar outreach: {e}")
        conn.rollback()

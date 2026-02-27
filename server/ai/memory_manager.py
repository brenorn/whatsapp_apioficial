from database.connection import db_manager
from typing import List, Dict

class MemoryManager:
    """Gerencia a janela de contexto curta do WhatsApp"""
    
    @staticmethod
    def get_context_history(phone: str, message_limit: int = 10) -> List[Dict]:
        """
        Recupera as últimas X interações do banco formatadas para LangChain 
        ou OpenAI ("user": "...", "assistant": "...")
        """
        conn = db_manager.connect()
        if not conn: return []
            
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) if hasattr(db_manager, 'psycopg2') else conn.cursor()
            
            # Ordenação ascendente para manter a linha do tempo [Velho -> Novo]
            query = """
                SELECT * FROM (
                    SELECT sender, message, created_at
                    FROM whatsapp_messages
                    WHERE phone = %s
                    ORDER BY created_at DESC LIMIT %s
                ) sub
                ORDER BY created_at ASC
            """
            cur.execute(query, (phone, message_limit))
            rows = cur.fetchall()
            
            history = []
            for row in rows:
                role = "user" if row[0] == "user" else "assistant"
                history.append({
                    "role": role,
                    "content": row[1]
                })
            
            return history
            
        except Exception as e:
            print(f"❌ [DB ALERT] Erro ao recuperar histórico para memória {phone}: {e}")
            return []

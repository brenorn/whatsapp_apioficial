import psycopg2
from psycopg2.extras import DictCursor
import os

class DatabaseConnection:
    """Singleton de conexão com o PostgreSQL para o módulo de Whatsapp"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.conn = None
        return cls._instance

    def connect(self):
        """Abre uma comunicação direta com o banco focado na performace"""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("⚠️ [DB] Nenhuma DATABASE_URL no .env. Ignorando conexão.")
            return None
            
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(db_url)
            return self.conn
        except Exception as e:
            print(f"❌ [DB FATAL] Erro ao conectar ao postgres: {e}")
            return None

    def close(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.close()

db_manager = DatabaseConnection()

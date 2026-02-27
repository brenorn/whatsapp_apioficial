import logging
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class DataAnalyst:
    """
    Cientista de Dados (Projeto 8).
    Transforma perguntas em linguagem natural em queries SQL precisas para o PostgreSQL.
    """

    @classmethod
    def generate_sql(cls, user_query: str) -> str:
        """
        Gera a query SQL baseada no schema simplificado das tabelas da clínica.
        """
        
        prompt = f"""
        Você é um Expert em PostgreSQL e Business Intelligence (BI).
        Sua missão é converter a pergunta do Chefe em uma Query SQL válida.

        SCHEMA DAS TABELAS:
        - messages (id, phone, message, sender, timestamp, msg_type)
        - orders (id, phone, total_value, status, created_at)
        - appointments (id, phone, date, time, status)

        DADOS ÚTEIS:
        - Status de orders: 'pending', 'paid', 'cancelled'.
        - Sender em messages: 'user' ou 'bot'.
        - Status em appointments: 'confirmed', 'cancelled', 'attended'.

        PERGUNTA DO CHEFE: "{user_query}"

        REGRAS DE OURO:
        1. Retorne APENAS o código SQL puro. Sem explicações ou markdown.
        2. Certifique-se de que os nomes das colunas e tabelas batem com o schema acima.
        3. Se a pergunta for sobre "faturamento", use SUM(total_value) na tabela orders onde status é 'paid'.
        4. Se a pergunta for sobre "quantidade", use COUNT(*).
        5. Sempre sanitize a query para evitar erros de sintaxe (sem ponto e vírgula no final se possível).

        QUERY SQL:
        """

        logger.info(f"📊 [DATA ANALYST] Traduzindo pergunta '{user_query}' em SQL...")
        
        try:
            sql = LLMFactory.generate(prompt, task_level="complex")
            # Cleanup para garantir que venha apenas o SQL (caso a LLM mande blocos de código)
            sql = sql.replace("```sql", "").replace("```", "").strip()
            return sql
        except Exception as e:
            logger.error(f"❌ [DATA ANALYST ERROR] Falha ao gerar SQL: {e}")
            return ""

import logging
import json
from ai.llm_factory import LLMFactory
from database.repository import execute_raw_bi_query
from core.config_manager import BusinessConfigManager

logger = logging.getLogger(__name__)

class BIOrchestrator:
    """
    Motor CEO Intelligence (Projeto 8).
    Converte perguntas em Linguagem Natural para Queries SQL no Banco Master.
    Gera resumos executivos baseados em dados reais.
    """

    SYSTEM_PROMPT = """
    Você é o Agente CEO Intelligence da MoveMind. 
    Sua missão é traduzir perguntas de negócios em queries PostgreSQL precisas.
    
    ESTRUTURA DO BANCO (Tabelas Disponíveis):
    - whatsapp_messages: (phone, message, sender, message_status, created_at)
    - negotiation_logs: (phone, original_value, final_value, status, created_at)
    - hot_leads: (phone, source, context, created_at)
    - ads_performance: (customer_id, stats -> JSONB, created_at)
    - nps_responses: (phone, score, feedback, created_at)
    - loyalty_accounts: (phone, xp, level)
    
    REGRAS CRÍTICAS:
    1. Responda APENAS com a query SQL em um bloco de código markdown.
    2. Use APENAS SELECT (Somente leitura). Nunca use DELETE, DROP ou UPDATE.
    3. Se não tiver certeza de qual tabela usar, peça clarificação no resumo, não invente.
    4. Use filtros de data (created_at) se o usuário mencionar "este mês", "hoje" ou "ontem".
    """

    @classmethod
    async def ask_data(cls, question: str) -> str:
        """
        Recebe uma pergunta humana, gera SQL, executa e devolve um resumo humanizado.
        """
        # 1. Obter contexto do negócio (DNS do setor)
        business_ctx = BusinessConfigManager.get_prompt_prefix()
        
        # 2. Gerar QUERY SQL via IA
        sql_prompt = f"""
        {business_ctx}
        Pergunta do CEO: "{question}"
        
        Gere a query SQL para responder a essa pergunta baseada nas tabelas acima.
        """
        
        logger.info(f"📊 [BI] Gerando SQL para: {question}")
        generated_sql_resp = LLMFactory.generate(
            sql_prompt, 
            task_level="complex", 
            system_instruction=cls.SYSTEM_PROMPT
        )
        
        # Extrair SQL do bloco markdown (se houver)
        sql_query = cls._extract_sql(generated_sql_resp)
        
        if not sql_query:
            return "Não consegui traduzir sua pergunta em uma análise técnica. Tente ser mais específico sobre o que deseja medir."

        # 3. Executar Query no Banco Master
        try:
            results = execute_raw_bi_query(sql_query)
            
            # 4. Gerar Insight Executivo baseado nos resultados
            insight_prompt = f"""
            {business_ctx}
            Pergunta Original: "{question}"
            Dados Brutos do Banco: {results}
            
            Gera um BRIEFING EXECUTIVO (2-3 linhas) resumindo esses dados de forma estratégica para o dono da empresa.
            """
            
            summary = LLMFactory.generate(insight_prompt, task_level="simple")
            return f"📊 **Resumo de Inteligência:**\n{summary}\n\n🔍 *Dados Técnicos:* {results}"
            
        except Exception as e:
            logger.error(f"❌ [BI Engine] Falha ao processar dados: {e}")
            return f"⚠️ Erro ao acessar a inteligência de dados: {str(e)}"

    @staticmethod
    def _extract_sql(text: str) -> str:
        """Extrai a query de dentro de blocos de código ```sql ... ```"""
        import re
        match = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Se não tiver markdown, tenta pegar o texto puro se parecer SQL
        if "SELECT" in text.upper():
            return text.strip()
        return ""

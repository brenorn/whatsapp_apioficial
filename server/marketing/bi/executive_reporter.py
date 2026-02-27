import logging
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class ExecutiveReporter:
    """
    Repórter Executivo (Projeto 8).
    Transforma resultados de banco de dados (tabelas/números) em insights de negócio.
    """

    @classmethod
    def format_insight(cls, raw_data: any, original_question: str) -> str:
        """
        Gera uma resposta amigável e estratégica para o dono ("Chefe").
        """
        
        prompt = f"""
        Você é o Consultor Estratégico da Clínica MoveMind.
        Seu objetivo é reportar os resultados ao "Chefe" (o dono da empresa) de forma clara, executiva e positiva.

        RESULTADOS BRUTOS DO BANCO:
        {raw_data}

        PERGUNTA ORIGINAL:
        "{original_question}"

        REGRAS DE COMUNICAÇÃO:
        1. Comece sempre com "Oi Chefe,".
        2. Explique o que o número significa no contexto do negócio.
        3. Se os números forem bons, comemore brevemente.
        4. Use emojis de negócios/finanças.
        5. Seja breve, mas informativo.
        6. Converta valores monetários para Real Brasileiro (R$).

        RESPOSTA EXECUTIVA:
        """

        logger.info(f"🎤 [EXECUTIVE REPORTER] Formatando insight para os dados: {raw_data}")
        
        try:
            return LLMFactory.generate(prompt, task_level="complex")
        except Exception as e:
            logger.error(f"❌ [REPORTER ERROR] {e}")
            return f"Oi Chefe, o resultado da sua consulta foi: {raw_data}."

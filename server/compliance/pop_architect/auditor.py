import logging
import json
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class POPAuditor:
    """
    Gestor de Qualidade de POPs.
    Realiza auditoria crítica para garantir conformidade e clareza.
    """

    def __init__(self):
        pass # LLMFactory é estática

    async def audit_pop(self, pop_content: str) -> dict:
        """
        Avalia a qualidade do POP e atribui um score de 0-10.
        """
        prompt = f"""
        Avalie a qualidade deste POP como um Gestor de ISO 9001:
        ---
        {pop_content[:5000]}
        ---
        
        Critérios:
        1. Clareza das instruções.
        2. Presença de KPIs.
        3. Identificação de riscos.
        4. Estrutura 5W2H.
        
        Retorne APENAS um JSON:
        {{
            "score": float,
            "feedback": "string",
            "needs_revision": bool,
            "improvement_points": ["point1", "point2"]
        }}
        """
        
        response_raw = LLMFactory.generate(prompt, task_level="complex")
        try:
            # Tenta extrair JSON da resposta da IA
            import re
            match = re.search(r'\{.*\}', response_raw, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {"score": 5.0, "feedback": "Falha na análise automática."}
        except:
            return {"score": 0.0, "feedback": "Erro de processamento."}

import logging
from typing import Dict, Any
from datetime import datetime
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class POPGenerator:
    """
    Motor de Geração de POPs com base em 13 seções (Projeto Elite).
    Suga a inteligência do projeto MOVE_POP original.
    """

    def __init__(self):
        pass # LLMFactory é estática

    async def generate_full_pop(self, topic: str, context: Dict[str, Any]) -> str:
        """
        Gera um documento POP completo estruturado.
        """
        sections = [
            "APRESENTAÇÃO", "OBJETIVO", "PESSOAS ENVOLVIDAS", "FLUXO DO PROCESSO",
            "PRÉ-REQUISITOS", "PROCESSO DETALHADO", "ERROS RECORRENTES", 
            "PROCESSOS POSTERIORES", "INDICADORES DE DESEMPENHO", "COMO IMPLEMENTAR",
            "GLOSSÁRIO", "ANEXO 01", "CONTROLE DE REVISÕES"
        ]
        
        full_markdown = f"# 📋 PROCEDIMENTO OPERACIONAL PADRÃO: {topic}\n"
        full_markdown += f"> **Data de Geração:** {datetime.now().strftime('%d/%m/%Y')}\n\n"

        # Chamada única para gerar o corpo principal (Economia de Tokens)
        prompt = f"""
        Aja como um Sênior Process Engineer. Gere um POP profissional para "{topic}".
        Contexto da Empresa: {context.get('company_profile', 'Clínica Médica')}
        
        O documento DEVE conter estas seções:
        {', '.join(sections)}
        
        Use a metodologia 5W2H para o Processo Detalhado.
        Seja técnico, direto e focado em segurança e eficiência.
        """
        
        body = LLMFactory.generate(prompt, task_level="complex")
        full_markdown += body
        
        return full_markdown

import logging
import json
from ai.llm_factory import LLMFactory
from ai.rag_manager import RAGManager

logger = logging.getLogger(__name__)

class HealthVaultEngine:
    """
    Motor de Inteligência Clínica (Projeto 22).
    Implementa RAG Médico e Guardrails de Segurança do Paciente.
    Objetivo: Prevenir erros de prescrição e resumir históricos.
    """

    SYSTEM_INSTRUCTION = """
    Aja como um Assistente de Decisão Clínica Sênior (MedGemma Core).
    Sua missão é a SEGURANÇA DO PACIENTE. 
    Você deve analisar o histórico clínico e o plano atual do médico para filtrar riscos.

    DIRETRIZES:
    1. Seja precavido: Se houver dúvida sobre alergia, alerte.
    2. Linguagem: Médica técnica para o doutor, mas explicativa.
    3. RAG: Baseie-se APENAS no histórico fornecido. Não alucine fatos.
    4. Prioridade: Alergias > Interações Medicamentosas > Histórico de Cirurgias.
    """

    @classmethod
    async def analyze_safety(cls, history: str, prescription_intent: str) -> str:
        """
        Analisa se uma prescrição pretendida é segura baseada no vault do paciente.
        """
        # 1. Busca Contexto Híbrido (Graph + SQL + Vector)
        hybrid_context = await RAGManager.hybrid_query(prescription_intent)
        
        prompt = f"""
        CONTEXTO HÍBRIDO DO PACIENTE (IA Intelligence):
        {hybrid_context}

        HISTÓRICO BRUTO:
        {history}

        INTENÇÃO DE PRESCRIÇÃO:
        "{prescription_intent}"

        Analise os dados acima procurando por conflitos. Se existir risco alérgico ou interação perigosa, emita um '⚠️ ALERTA CRÍTICO'. 
        Caso contrário, forneça um '✅ PARECER DE SEGURANÇA'.
        """

        logger.info("🏥 [HEALTH VAULT] Realizando auditoria clínica de segurança...")
        
        return LLMFactory.generate(
            prompt, 
            task_level="complex", 
            system_instruction=cls.SYSTEM_INSTRUCTION
        )

    @classmethod
    async def generate_doctor_briefing(cls, history: str) -> str:
        """
        Gera um resumo executivo para o médico ler em 30 segundos antes de entrar na sala.
        """
        prompt = f"Gere um MEDICAL FLASH BRIEFING (1 parágrafo) focado em riscos e histórico relevante:\n{history}"
        
        return LLMFactory.generate(
            prompt, 
            task_level="complex", 
            system_instruction=cls.SYSTEM_INSTRUCTION
        )

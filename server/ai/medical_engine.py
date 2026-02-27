import logging
from typing import Dict, Any, List
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class MedicalIntelService:
    """
    Serviço modular para Apoio à Decisão Médica (Health Vault).
    Utiliza MedGemma e RAG para segurança do paciente.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()

    async def get_patient_summary_for_doctor(self, patient_phone: str) -> str:
        """
        Retorna o 'Flash Medical Briefing' para o médico antes da consulta.
        """
        history = self.repo.get_medical_history(patient_phone)
        
        prompt = f"""
        Aja como um Assistente de Clínica Médica de Elite. 
        Resuma o histórico clínico para o doutor:
        "{history}"
        
        Foques: Alergias, Últimos procedimentos, Medicamentos em uso.
        Seja extremamente conciso e destaque Riscos em Negrito.
        """
        summary = await self.llm.generate_text(prompt)
        return summary

    async def check_contraindications(self, patient_phone: str, prescribed_med: str):
        """
        Cruza o medicamento prescrito com as alergias do paciente no banco.
        """
        patient_data = self.repo.get_medical_history(patient_phone)
        
        prompt = f"""
        PACIENTE: {patient_data}
        PRESCRIÇÃO ATUAL: {prescribed_med}
        
        Existe alguma contraindicação ou risco alérgico? 
        Responda apenas "⚠️ ALERTA: [MOTIVO]" ou "✅ SEGURO".
        """
        # Aqui usaríamos o MedGemma via Vertex AI se disponível
        safety_check = await self.llm.generate_text(prompt)
        return safety_check

    def log_clinical_event(self, patient_id: str, event_type: str, data: dict):
        self.repo.log_medical_event(patient_id, event_type, data)

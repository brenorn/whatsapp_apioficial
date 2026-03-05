import logging
from typing import Dict, Any, List
from database.repository import Repository
from ai.llm_factory import LLMFactory
from ai.health_vault_engine import HealthVaultEngine

logger = logging.getLogger(__name__)

class MedicalIntelService:
    """
    Serviço modular para Apoio à Decisão Médica (Health Vault).
    Utiliza MedGemma e RAG para segurança do paciente.
    """

    def __init__(self):
        self.repo = Repository()

    async def get_patient_summary_for_doctor(self, patient_phone: str) -> str:
        """
        Retorna o 'Flash Medical Briefing' para o médico antes da consulta.
        """
        history = self.repo.get_medical_history(patient_phone)
        return await HealthVaultEngine.generate_doctor_briefing(history)

    async def check_contraindications(self, patient_phone: str, prescribed_med: str) -> str:
        """
        Cruza o medicamento prescrito com as alergias do paciente no banco.
        """
        history = self.repo.get_medical_history(patient_phone)
        return await HealthVaultEngine.analyze_safety(history, prescribed_med)

    def log_clinical_event(self, patient_id: str, event_type: str, data: dict):
        self.repo.log_medical_event(patient_id, event_type, data)

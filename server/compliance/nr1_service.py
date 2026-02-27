import logging
from datetime import datetime
from typing import Dict, Any, List
from server.database.repository import Repository
from server.ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class NR1ComplianceService:
    """
    Serviço Independente para Gestão de Compliance NR-01 e Saúde Psicossocial.
    Responsável por gerenciar ciclos de auditoria e analisar riscos humanos.
    """

    def __init__(self):
        self.repo = Repository()
        self.llm = LLMFactory.get_instance()

    async def start_audit_cycle(self, admin_phone: str, department: str) -> str:
        """
        Inicia um novo ciclo de monitoramento para um departamento específico.
        """
        cycle_id = self.repo.create_nr1_cycle(department, "OPEN")
        logger.info(f"Ciclo NR1 {cycle_id} iniciado por {admin_phone}")
        return f"🚀 Ciclo de Compliance NR-01 iniciado para o setor: {department}. Os colaboradores serão notificados."

    async def process_response(self, worker_phone: str, response_data: Dict[str, Any]):
        """
        Processa e armazena a resposta de um colaborador, analisando o risco imediato.
        """
        # 1. Salva a resposta bruta
        self.repo.save_nr1_response(worker_phone, response_data)
        
        # 2. IA analisa o risco psicossocial baseado no tom da resposta
        prompt = f"""
        Analise a seguinte resposta de um colaborador em uma auditoria NR-01:
        "{response_data.get('text')}"
        
        Identifique:
        1. Nível de Estresse (0-10)
        2. Presença de sinais de Burnout (Sim/Não)
        3. Necessidade de intervenção humana (Sim/Não)
        
        Retorne apenas em JSON.
        """
        analysis = await self.llm.generate_structured(prompt)
        
        # 3. Se houver risco alto, dispara alerta
        if analysis.get("urgency") == "High":
            await self.trigger_burnout_alert(worker_phone, analysis)

    async def trigger_burnout_alert(self, worker_phone: str, analysis: Dict):
        """Dispara um alerta confidencial para o ADMIN_PHONE."""
        logger.warning(f"⚠️ RISCO DETECTADO: Colaborador {worker_phone} apresenta sinais de risco psicossocial.")
        # Lógica de envio via Cloud Client aqui

import os
import yaml
import logging
from typing import Dict, Any, Optional
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class CrewFactory:
    """
    Motor Declarativo de Agentes Multi-Especialistas (CrewAI Style).
    Lê os perfis psiciológicos (agents.yaml) e as missões (tasks.yaml) 
    para disparar chamadas cirurgicamente isoladas para a GenAI, 
    sem misturar contextos no Monolito Principal.
    """
    
    _agents: Dict[str, Any] = {}
    _tasks: Dict[str, Any] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        """Carrega os YAMLs em memória (Singleton-like Lazy Load)"""
        if cls._initialized:
            return
            
        base_dir = os.path.dirname(__file__)
        agents_path = os.path.join(base_dir, "config", "agents.yaml")
        tasks_path = os.path.join(base_dir, "config", "tasks.yaml")
        
        try:
            with open(agents_path, 'r', encoding='utf-8') as f:
                cls._agents = yaml.safe_load(f) or {}
                
            with open(tasks_path, 'r', encoding='utf-8') as f:
                cls._tasks = yaml.safe_load(f) or {}
                
            cls._initialized = True
            logger.info("🧠 [CREW FACTORY] Agentes Declarativos YAML Carregados e Treinados com Sucesso!")
        except Exception as e:
            logger.error(f"❌ [CREW FACTORY FATAL] Falha ao carregar yaml de inteligência: {e}")

    @classmethod
    def execute_task(cls, task_id: str, context_payload: Any = None) -> str:
        """
        Engatilha um Especialista isolado para resolver um problema único.
        Ex: task_id = 'transcribe_patient_audio'
        """
        cls.initialize()
        
        task_info = cls._tasks.get(task_id)
        if not task_info:
            logger.warning(f"⚠️ Task {task_id} não catalogada em tasks.yaml.")
            return f"[Task '{task_id}' Indisponível]"
            
        agent_id = task_info.get("agent")
        agent_profile = cls._agents.get(agent_id)
        
        if not agent_profile:
            logger.warning(f"⚠️ Agente {agent_id} desconhecido ou demitido em agents.yaml.")
            return "[Agente Indisponível]"
            
        logger.info(f"👔 [CREW AI] Task '{task_id}' delegada para -> {agent_profile.get('name')}")
        
        # 1. Cibersegurança & Regras da Persona
        system_instruction = (
            f"Você é: {agent_profile.get('name')}\n"
            f"Cargo: {agent_profile.get('role')}\n"
            f"Personalidade e Regra de Ouro:\n{agent_profile.get('backstory')}\n\n"
            f"Objetivo Máximo desta resposta:\n{agent_profile.get('goal')}"
        )
        
        # 2. A Missão e o Contexto Variável (O Áudio, A Conversa, O Carrinho)
        prompt = (
            f"Instrução Atual Escrita pelo Tech Lead:\n{task_info.get('description')}\n"
            f"Saída Esperada Exatamente:\n{task_info.get('expected_output')}\n\n"
            f"=== CONTEXTO DA REQUISIÇÃO ===\n{context_payload}"
        )
        
        # 3. Disparo usando Factory (Reduzindo o Custo de Tokens)
        # Identificando a task nivel (pro ou flash dependendo da persona)
        model_tier = "complex" if "pro" in str(agent_profile.get("model", "")).lower() else "simple"
        
        # Usamos o LLMFactory ja blindado pela arquitetura BMAD
        result_text = LLMFactory.generate(
            prompt=prompt,
            task_level=model_tier,
            system_instruction=system_instruction,
            temperature=0.3
        )
        
        return result_text

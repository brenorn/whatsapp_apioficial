import os
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BusinessConfigManager:
    """
    O Coração da Adaptabilidade (Agnostic Engine).
    Lê o perfil da empresa e injeta nos 25 microserviços.
    """
    
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "business_profile.yaml")

    @classmethod
    def get_business_context(cls) -> Dict[str, Any]:
        """Retorna o perfil completo da empresa para injetar no Prompt System."""
        if not os.path.exists(cls.CONFIG_PATH):
            cls._generate_default_config()
            
        try:
            with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"❌ Erro ao ler Perfil de Negócio: {e}")
            return {"sector": "General", "company_name": "MoveMind Client"}

    @classmethod
    def _generate_default_config(cls):
        """Cria um template inicial para o usuário adaptar para qualquer setor."""
        default = {
            "company_name": "MoveMind Inteligência",
            "sector": "Medicina/Clínica", # Ex: Advocacia, Imobiliária, E-commerce
            "tone_of_voice": "Profissional, Empático e Técnico",
            "customer_label": "Paciente", # Ex: Cliente, Aluno, Lead, Réu
            "core_service_label": "Consulta", # Ex: Contrato, Aula, Venda
            "critical_rules": [
                "Nunca prometer curas milagrosas",
                "Sempre validar dados sensíveis",
                "Encaminhar para humano em caso de emergência"
            ],
            "ai_persona": "Você é um Consultor Sênior especializado no setor definido acima."
        }
        with open(cls.CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(default, f, allow_unicode=True)

    @classmethod
    def get_prompt_prefix(cls) -> str:
        """Gera o bloco de texto que 'molda' a mente da IA para o setor correto."""
        ctx = cls.get_business_context()
        prefix = f"""
        CONTEXTO DE NEGÓCIO ATUAL:
        Empresa: {ctx.get('company_name')}
        Setor: {ctx.get('sector')}
        Tom de Voz: {ctx.get('tone_of_voice')}
        Nomenclatura: Chamamos nossos clientes de '{ctx.get('customer_label')}' e nosso serviço principal de '{ctx.get('core_service_label')}'.
        
        REGRAS DE OURO:
        {chr(10).join(['- ' + r for r in ctx.get('critical_rules', [])])}
        """
        return prefix

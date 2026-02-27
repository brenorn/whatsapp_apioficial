import logging
from typing import Dict, Any
from server.database.repository import Repository

logger = logging.getLogger(__name__)

class LoyaltyService:
    """
    Serviço modular para Gestão de Fidelidade e Gamificação.
    Lida com XP, Níveis e Recompensas.
    """

    def __init__(self):
        self.repo = Repository()

    async def add_xp(self, phone: str, amount: int, reason: str) -> Dict[str, Any]:
        """
        Adiciona XP ao perfil do paciente e verifica se houve "Level Up".
        """
        logger.info(f"✨ Adicionando {amount} XP para {phone} (Motivo: {reason})")
        
        # 1. Busca saldo atual
        current_data = self.repo.get_loyalty_data(phone)
        new_xp = current_data['xp'] + amount
        
        # 2. Lógica de Nível
        old_level = current_data['level']
        new_level = self._calculate_level(new_xp)
        
        # 3. Salva no banco
        self.repo.update_loyalty_xp(phone, new_xp, new_level)
        
        return {
            "previous_level": old_level,
            "current_level": new_level,
            "total_xp": new_xp,
            "leveled_up": new_level != old_level
        }

    async def get_status_message(self, phone: str) -> str:
        """Retorna uma mensagem motivadora sobre o status do programa."""
        data = self.repo.get_loyalty_data(phone)
        return f"🏆 *SEU STATUS:* Nível {data['level']}\n✨ XP: {data['xp']}\n💡 Dica: Falta pouco para você chegar no nível Platinum!"

    def _calculate_level(self, xp: int) -> str:
        if xp < 500: return "Bronze"
        if xp < 1500: return "Silver"
        if xp < 4000: return "Gold"
        return "Platinum"

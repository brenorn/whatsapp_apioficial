import logging
import os
from typing import Dict, Any
from compliance.pop_architect.generator import POPGenerator
from compliance.pop_architect.auditor import POPAuditor
from compliance.pop_architect.visualizer import MiroVisualizer

logger = logging.getLogger(__name__)

class POPArchitectService:
    """
    Orquestrador Elite de POPs (Suga tudo do MOVE_POP).
    Consolida Geração, Auditoria e Visualização.
    """

    def __init__(self):
        self.generator = POPGenerator()
        self.auditor = POPAuditor()
        self.visualizer = MiroVisualizer()
        # Garante o path absoluto para evitar erros de CWD
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.output_dir = os.path.join(base_path, "assets", "pop_reports")

    async def create_elite_pop(self, phone: str, topic: str) -> str:
        """
        Gera um POP completo, audita a qualidade e prepara para o Miro.
        """
        logger.info(f"📋 [POP] Iniciando construção elite para {topic}")
        
        # 1. Geração (13 Seções)
        context = {"company_profile": "Clínica Médica de Especialidades"}
        pop_content = await self.generator.generate_full_pop(topic, context)
        
        # 2. Auditoria de Qualidade
        audit = await self.auditor.audit_pop(pop_content)
        
        # 3. Preparação Visual
        miro_link = await self.visualizer.create_process_board(topic, pop_content)
        
        # 4. Formata Resposta final para o WhatsApp
        response = f"📋 *POP CONCLUÍDO (PADRÃO ELITE):* {topic}\n\n"
        response += f"⭐ *Score de Qualidade:* {audit.get('score')}/10\n"
        response += f"📝 *Status:* {'Aprovado' if audit.get('score') > 7 else 'Revisão Necessária'}\n"
        response += f"💡 *Dica:* {audit.get('feedback')[:100]}...\n\n"
        response += f"🎨 *Fluxo Visual:* {miro_link}\n\n"
        response += "_(O PDF completo foi enviado para o diretório de ativos da empresa)_"
        
        # Salva o arquivo fisicamente
        self._save_to_disk(topic, pop_content)
        
        return response

    def _save_to_disk(self, topic: str, content: str):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        filename = os.path.join(self.output_dir, f"POP_{topic.replace(' ', '_')}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    async def start_5w2h_interrogation(self, topic: str) -> str:
        """Fallback para manter compatibilidade com o interceptador anterior"""
        return await self.create_elite_pop("system", topic)

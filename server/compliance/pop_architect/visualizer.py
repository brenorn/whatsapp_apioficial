import logging
import os
import httpx
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MiroVisualizer:
    """
    Integrador com a API do Miro V2 para visualização de Processos.
    Transforma POPs textuais do 5W2H em quadros visuais com Sticky Notes e Conectores.
    """

    def __init__(self):
        self.api_token = os.getenv("MIRO_API_TOKEN")
        self.base_url = "https://api.miro.com/v2"

    async def create_process_board(self, pop_title: str, pop_content: str) -> str:
        """
        Cria um quadro no Miro, extrai as etapas do POP e gera o fluxograma.
        """
        if not self.api_token:
            logger.warning("⚠️ Miro API Token não configurado.")
            return "Miro Token Missing"

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        async with httpx.AsyncClient() as client:
            try:
                # 1. Criar o Board
                board_data = {
                    "name": f"POP: {pop_title}",
                    "policy": {"permissionsPolicy": {"collaborationToolsFamily": "all"}}
                }
                board_res = await client.post(f"{self.base_url}/boards", headers=headers, json=board_data)
                board_res.raise_for_status()
                board_id = board_res.json()["id"]
                board_url = board_res.json()["viewLink"]

                # 2. Extrair etapas (Parsing do 5W2H)
                steps = self.extract_steps_for_miro(pop_content)
                
                # 3. Criar Sticky Notes e Conectar em linha
                prev_item_id = None
                x_pos = 0
                
                for step in steps:
                    sticky_data = {
                        "data": {"content": f"<b>{step['phase']}</b><br>{step['how']}"},
                        "position": {"x": x_pos, "y": 0}
                    }
                    sticky_res = await client.post(f"{self.base_url}/boards/{board_id}/sticky_notes", headers=headers, json=sticky_data)
                    sticky_res.raise_for_status()
                    current_item_id = sticky_res.json()["id"]

                    # Conectar com o anterior
                    if prev_item_id:
                        conn_data = {
                            "startItem": {"id": prev_item_id},
                            "endItem": {"id": current_item_id}
                        }
                        await client.post(f"{self.base_url}/boards/{board_id}/connectors", headers=headers, json=conn_data)
                    
                    prev_item_id = current_item_id
                    x_pos += 300 # Espaçamento horizontal

                return board_url

            except Exception as e:
                logger.error(f"❌ [MIRO] Erro na integração: {str(e)}")
                return f"Erro na integração com Miro: {str(e)}"

    def extract_steps_for_miro(self, pop_content: str) -> List[Dict[str, str]]:
        """
        Extrai as etapas do 5W2H de dentro do Markdown do POP.
        """
        steps = []
        # Procura por linhas de tabela Markdown que contenham o 5W2H
        # Formato esperado: | Fase | O que | Por que | Quem | Onde | Quando | Como | Quanto |
        matches = re.findall(r"\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", pop_content)
        
        for m in matches:
            phase = m[0].strip()
            if phase.lower() in ["fase", "etapa", "---", "objective"]: continue # Pula cabeçalhos
            
            steps.append({
                "phase": phase,
                "how": m[6].strip()
            })
        
        # Fallback se não encontrar tabela: pega bullets
        if not steps:
            bullets = re.findall(r"-\sPasso\s\d+:\s*(.*)", pop_content)
            for b in bullets:
                steps.append({"phase": b, "how": "Executar conforme descrito."})

        return steps[:10] # Limite de 10 post-its para não poluir

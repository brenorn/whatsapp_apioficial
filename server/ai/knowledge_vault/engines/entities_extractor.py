import json
import os
import re
import time
import logging
from typing import List, Dict, Any, Tuple, Optional
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class EntitiesExtractor:
    """
    EntitiesExtractor adaptado do sistema GraphRAG do Sandeco.
    Responsável por extrair ENTIDADES e RELAÇÕES de fragmentos de texto.
    """

    def __init__(
        self,
        schema_data: Dict[str, Any],
        model_name: str = "gemini-2.0-flash",
        reflection: bool = False,
        max_gleaning_steps: int = 1,
    ):
        self.model_name = model_name
        self.reflection = reflection
        self.max_gleaning_steps = max_gleaning_steps
        self.entity_types = list(schema_data.get("tipos_entidade", {}).keys())
        self.rel_types = list(schema_data.get("tipos_relacionamento", {}).keys())

    def extract(self, text: str) -> Dict[str, List[Dict]]:
        """API Principal de extração."""
        data = self._call_llm_for_extraction(text)
        
        if self.reflection:
            data = self._execute_gleaning(text, data)

        return self._normalize_data(data)

    def _call_llm_for_extraction(self, text: str, prev_data: Dict = None) -> Dict:
        prompt = self._build_prompt(text, prev_data)
        response = LLMFactory.generate(prompt, task_level="complex")
        parsed = self._robust_json_parse(response)
        return parsed

    def _execute_gleaning(self, text: str, data: Dict) -> Dict:
        """Processo de 'peneira' para encontrar o que a LLM esqueceu."""
        for i in range(self.max_gleaning_steps):
            prompt = f"Temos {len(data.get('entities', []))} entidades. Falta algo importante neste texto? Responda SIM ou NAO.\n\nTEXTO: {text[:500]}"
            check = LLMFactory.generate(prompt, task_level="simple")
            
            if "SIM" not in check.upper():
                break

            new_data = self._call_llm_for_extraction(text, prev_data=data)
            if not new_data.get("entities", []):
                break

            for k in ["entities", "relationships"]:
                data[k].extend(new_data.get(k, []))
        
        return data

    def _build_prompt(self, text: str, prev_data: Dict = None) -> str:
        context = ""
        if prev_data:
            names = ", ".join(e.get("name", "") for e in prev_data.get("entities", []))
            context = f"Já extraímos: {names}. Foque em novas entidades e relações."

        return f"""
        Você é um Extrator GraphRAG de Elite.
        Sua tarefa é extrair ENTIDADES e RELAÇÕES do texto abaixo.
        
        TIPOS DE ENTIDADE PERMITIDOS: {self.entity_types}
        TIPOS DE RELAÇÃO PERMITIDOS: {self.rel_types}
        
        {context}
        
        RETORNE APENAS JSON NO FORMATO:
        {{
          "entities": [{{ "name": "NOME", "type": "TIPO", "description": "Breve descrição" }}],
          "relationships": [{{ "source": "NOME1", "target": "NOME2", "type": "TIPO", "description": "Relato", "strength": 1-10 }}]
        }}
        
        TEXTO:
        {text}
        """

    def _robust_json_parse(self, text: str) -> Dict:
        try:
            match = re.search(r"(\{[\s\S]*\})", text)
            if match:
                return json.loads(match.group(1))
            return {}
        except Exception as e:
            logger.warning(f"Falha no parse de JSON de extração: {e}")
            return {}

    def _normalize_data(self, data: Dict) -> Dict:
        """Garante que os dados seguem o padrão esperado."""
        normalized = {"entities": [], "relationships": []}
        
        for e in data.get("entities", []):
            if "name" in e and "type" in e:
                e["name"] = str(e["name"]).upper().strip()
                normalized["entities"].append(e)
                
        for r in data.get("relationships", []):
            if "source" in r and "target" in r:
                r["source"] = str(r["source"]).upper().strip()
                r["target"] = str(r["target"]).upper().strip()
                normalized["relationships"].append(r)
                
        return normalized

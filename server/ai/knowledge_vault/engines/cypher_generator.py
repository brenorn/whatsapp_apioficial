import re
from typing import Dict, List, Any

class CypherGenerator:
    """Traduz o snapshot de conhecimento em comandos Cypher para o Neo4j."""

    def generate(self, snapshot: Dict[str, Any], domain: str = "GLOBAL") -> str:
        lines = []
        
        # 1. Gerar Nós
        for idx, e in enumerate(snapshot.get("entities", []), 1):
            name = str(e['name']).replace("'", "\\'")
            etype = re.sub(r'[^A-Z0-9_]', '_', str(e['type']).upper())
            desc = str(e.get('description', '')).replace("'", "\\'")
            
            # Adicionamos o label do domínio (Area X) para isolamento
            domain_label = re.sub(r'[^A-Z0-9_]', '_', domain.upper())
            
            line = (
                f"MERGE (e{idx}:ENTITY:{etype}:{domain_label} {{name: '{name}'}}) "
                f"SET e{idx}.description = '{desc}', e{idx}.domain = '{domain}', e{idx}.updated_at = timestamp();"
            )
            lines.append(line)

        # 2. Gerar Relações
        # Precisamos de um novo loop para garantir que os nós existam ANTES de criar arestas
        for idx, r in enumerate(snapshot.get("relationships", []), 1):
            src = str(r['source']).replace("'", "\\'")
            tgt = str(r['target']).replace("'", "\\'")
            rtype = re.sub(r'[^A-Z0-9_]', '_', str(r['type']).upper())
            desc = str(r.get('description', '')).replace("'", "\\'")
            strength = r.get('strength', 5)

            line = (
                f"MATCH (a {{name: '{src}'}}), (b {{name: '{tgt}'}}) "
                f"MERGE (a)-[r{idx}:{rtype} {{domain: '{domain}'}}]->(b) "
                f"SET r{idx}.description = '{desc}', r{idx}.strength = {strength};"
            )
            lines.append(line)

        return "\n".join(lines)

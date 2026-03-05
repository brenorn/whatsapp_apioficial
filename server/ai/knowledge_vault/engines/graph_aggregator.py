from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Set
import re

def _norm(s: str) -> str:
    return str(s).strip().upper()

@dataclass
class _AggEntity:
    name: str
    type: str = "UNKNOWN"
    description: str = ""
    freq: int = 0

    def absorb(self, type_: str, description: str):
        self.freq += 1
        if self.type == "UNKNOWN" or len(type_) > len(self.type):
            self.type = type_
        if len(description) > len(self.description):
            self.description = description

@dataclass
class _AggRel:
    source: str
    target: str
    type: str
    description: str = ""
    strength_sum: float = 0.0
    count: int = 0

    def absorb(self, description: str, strength: float):
        self.count += 1
        self.strength_sum += float(strength)
        if len(description) > len(self.description):
            self.description = description

class GraphAggregator:
    """Consolida extrações de múltiplos chunks em um snapshot único."""

    def __init__(self):
        self.entities: Dict[str, _AggEntity] = {}
        self.rels: Dict[Tuple[str, str, str], _AggRel] = {}

    def add_extraction(self, data: Dict[str, Any]):
        for e in data.get("entities", []):
            name = _norm(e.get("name"))
            if not name: continue
            if name not in self.entities:
                self.entities[name] = _AggEntity(name=name)
            self.entities[name].absorb(e.get("type", "UNKNOWN"), e.get("description", ""))

        for r in data.get("relationships", []):
            src = _norm(r.get("source"))
            tgt = _norm(r.get("target"))
            rtype = _norm(r.get("type", "RELATION"))
            if not src or not tgt: continue
            
            key = (src, tgt, rtype)
            if key not in self.rels:
                self.rels[key] = _AggRel(source=src, target=tgt, type=rtype)
            self.rels[key].absorb(r.get("description", ""), r.get("strength", 5))

    def snapshot(self) -> Dict[str, Any]:
        return {
            "entities": [
                {"name": e.name, "type": e.type, "description": e.description, "freq": e.freq}
                for e in self.entities.values()
            ],
            "relationships": [
                {
                    "source": r.source, 
                    "target": r.target, 
                    "type": r.type, 
                    "description": r.description, 
                    "strength": round(r.strength_sum / r.count, 2) if r.count > 0 else 5
                }
                for r in self.rels.values()
            ]
        }

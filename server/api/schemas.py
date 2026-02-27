from pydantic import BaseModel
from typing import Optional, List, Any

# ==========================================
# MODELOS DE RECEPÇÃO DA META (WEBHOOK)
# ==========================================

class TextObject(BaseModel):
    body: str

class MessageObject(BaseModel):
    from_: str  # mapeado de 'from' no payload
    id: str
    timestamp: str
    type: str
    text: Optional[TextObject] = None

class ValueObject(BaseModel):
    messaging_product: str
    metadata: dict
    contacts: Optional[List[dict]] = None
    messages: Optional[List[dict]] = None

class ChangeObject(BaseModel):
    value: ValueObject
    field: str

class EntryObject(BaseModel):
    id: str
    changes: List[ChangeObject]

class MetaWebhookPayload(BaseModel):
    """Esquema oficial padronizado para Inbound da Meta API"""
    object: str
    entry: List[EntryObject]

# ==========================================
# MODELOS DE BANCO DE DADOS (MONITOR / DB)
# ==========================================
class LogMessageModel(BaseModel):
    phone: str
    message: str
    sender: str  # deve ser 'user', 'bot' ou 'me'
    message_type: str = "text"
    metadata: Optional[dict] = {}

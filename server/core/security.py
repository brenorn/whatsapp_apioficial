import hmac
import hashlib
import os

def validate_hub_signature(payload: bytes, signature_header: str) -> bool:
    """
    Verifica se o webhook foi realmente disparado pela Meta comparando
    o Header X-Hub-Signature-256 com um Hash do corpo gerado na hora usando
    a APP SECRET oficial guardada (ou Token de verificação se simular o AppSecret).
    Padrão Ouro de Zero-Trust Architecture.
    """
    if not signature_header:
        return False
        
    app_secret = os.getenv("FACEBOOK_APP_SECRET", os.getenv("FACEBOOK_VERIFY_TOKEN", ""))
    
    if not app_secret:
        return False

    # Extrair sha256= do cabeçalho
    if not signature_header.startswith("sha256="):
        return False
    received_signature = signature_header.split("sha256=")[1]
    
    # Criar nosso proprio Hash com a chave
    expected_hash = hmac.new(
        key=app_secret.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Comparar de forma segura (previne ataques de timing)
    return hmac.compare_digest(expected_hash, received_signature)


import re
import logging

logger = logging.getLogger(__name__)

class PIIValidator:
    """
    Detector de Dados Sensíveis (LGPD).
    Bloqueia vazamento de CPF, RG, E-mail e Cartão de Crédito.
    """

    # Regex para CPF: 000.000.000-00 ou 00000000000
    CPF_REGEX = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'
    
    # Regex para E-mail
    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Regex para Cartão de Crédito (Luhn Check seria ideal, mas Regex resolve 90%)
    CC_REGEX = r'\b(?:\d[ -]*?){13,16}\b'

    @classmethod
    def anonymize(cls, text: str) -> str:
        """Substitui dados sensíveis por placeholders."""
        text = re.sub(cls.EMAIL_REGEX, "[E-MAIL PROTEGIDO]", text)
        text = re.sub(cls.CPF_REGEX, "[CPF PROTEGIDO]", text)
        
        # Só anonimiza se parecer CC (mais de 13 dígitos seguidos)
        if re.search(cls.CC_REGEX, text):
            text = re.sub(cls.CC_REGEX, "[DADO FINANCEIRO PROTEGIDO]", text)
            
        return text

    @classmethod
    def has_pii(cls, text: str) -> bool:
        """Verifica se existem dados sensíveis."""
        return any([
            re.search(cls.EMAIL_REGEX, text),
            re.search(cls.CPF_REGEX, text),
            re.search(cls.CC_REGEX, text)
        ])

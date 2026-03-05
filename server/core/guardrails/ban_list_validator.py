import logging

logger = logging.getLogger(__name__)

class BanListValidator:
    """
    Filtro de Toxicidade e Palavras Proibidas.
    Mantém o decoro e o tom profissional da clínica.
    """

    BANNED_WORDS = [
        "PORRA", "MERDA", "CARALHO", "PUTA", "DESGRAÇA", 
        "LIXO", "IDIOTA", "INCOMPETENTE", "ESTUPRO", "MATAR"
    ]

    @classmethod
    def validate(cls, text: str) -> bool:
        """
        Retorna True se o texto estiver limpo.
        False se contiver termos ofensivos.
        """
        text_upper = text.upper()
        for word in cls.BANNED_WORDS:
            if word in text_upper:
                logger.warning(f"🚫 [BANLIST] Palavra proibida detectada: {word}")
                return False
        return True

    @classmethod
    def censor(cls, text: str) -> str:
        """Substitui palavras ofensivas por asteriscos."""
        text_upper = text.upper()
        clean_text = text
        for word in cls.BANNED_WORDS:
            if word in text_upper:
                # Caso queira censurar em vez de bloquear
                import re
                clean_text = re.sub(re.escape(word), "*" * len(word), clean_text, flags=re.IGNORECASE)
        return clean_text

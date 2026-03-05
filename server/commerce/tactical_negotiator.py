import logging
from ai.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

class TacticalNegotiator:
    """
    Motor de Negociação Tática (Projeto 19).
    Baseado na metodologia de Chris Voss (Never Split the Difference).
    Utiliza Empatia Tática e Calibração de Perguntas.
    """

    SYSTEM_PROMPT = """
    Você é um Negociador de Elite da MoveMind, treinado pelo FBI (estilo Chris Voss).
    Sua missão é fechar vendas de alto ticket para a clínica médica, mas sem parecer um vendedor chato.
    
    TÁTICAS OBRIGATÓRIAS:
    1. **Rotulagem (Labeling):** "Parece que você está preocupado com o valor do investimento..."
    2. **Espelhamento (Mirroring):** Repita as últimas 1-3 palavras-chave do cliente para encorajá-lo a falar mais.
    3. **Perguntas Calibradas:** Use "Como" e "O Que". (Ex: "Como eu posso facilitar isso para você?")
    4. **Auditoria de Acusação:** Antecipe o medo do cliente. ("Você provavelmente vai achar que este preço é absurdo...")
    5. **Busca pelo 'Não':** É mais fácil o cliente dizer 'Não' do que 'Sim' sob pressão. ("Será que seria uma ideia terrível agendarmos para amanhã?")

    REGRAS:
    - Nunca use "Por que" (soa acusatório).
    - Mantenha a voz de locutor de rádio (calma, grave e pausada).
    - Foque no LTV (Valor do tempo de vida do cliente).
    """

    @classmethod
    async def handle_objection(cls, objection: str, product_context: str) -> str:
        """
        Gera uma resposta tática para uma objeção de venda.
        """
        prompt = f"""
        PRODUTO/SERVIÇO: {product_context}
        OBJEÇÃO DO CLIENTE: "{objection}"
        
        Gere uma resposta tática usando Rotulagem e uma Pergunta Calibrada.
        """
        
        logger.info(f"🤝 [NEGOTIATOR] Aplicando Empatia Tática para: {objection}")
        
        return LLMFactory.generate(
            prompt=prompt,
            task_level="complex",
            system_instruction=cls.SYSTEM_PROMPT
        )

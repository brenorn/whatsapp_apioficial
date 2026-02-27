from .intent_analyzer import IntentAnalyzer
from .memory_manager import MemoryManager
from .llm_factory import LLMFactory
from .knowledge_manager import KnowledgeManager
import json

def generate_ai_response(text: str, phone: str = "1234") -> str:
    """
    O Cerebro de Conexao com as APIs (Gemini, Langchain, etc.)
    Abaixo e o esqueleto de onde o desenvolvedor escrevera o RAG definitivo.
    """
    
    # 1. Recuperar contexto do banco (Memória da Sessão)
    history = MemoryManager.get_context_history(phone, message_limit=5)
    
    # 2. Analisar intencao (Fast Path Anti-Desperdício de Tokens)
    intent_data = IntentAnalyzer.identify_intent(text)
    
    # Fast Path: Se for crise, a IA é bloqueada na ponta e envia socorro
    if intent_data.get("is_crisis"):
        return "Notamos que pode ser uma urgência. Por favor, procure o pronto-socorro mais próximo imediatamente, não possuímos atendimento de crise virtual."
    
    # Fast_Path: Se enviou um simples Sim/Ok, não chama LLM pesado
    if IntentAnalyzer.is_fast_path(text):
         # Como o Lead enviou um padrão óbvio, repassamos para a Factory barata (Simple) fechar o ticket.
         return LLMFactory.generate(
             prompt=f"O paciente disse '{text}'. Agradeça brevemente e encerre a interação gentilmente.",
             task_level="simple",
             temperature=0.2
         )
         
    # 3. EXTRAIR RAG DA CLÍNICA (O Cérebro da Secretária)
    knowledge_base = KnowledgeManager.get_full_context()
         
    # 4. CONSTRUÇÃO DO PROMPT
    # Formatação limpa do histórico em formato TXT que a maioria dos LLMs adora
    history_str = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history])
    
    system_prompt = (
        f"Você é a secretária virtual acolhedora da Clínica MoveMind.\n"
        f"Abaixo estão todas as regras comerciais, de agenda e de preço que você sabe e domina:\n\n"
        f"=== BASE DE DADOS (CONHECIMENTO GERAL) ===\n"
        f"{knowledge_base}\n"
        f"================================\n\n"
        f"Nunca invente informações fora dessa base de dados acima. Caso o cliente pergunte algo "
        f"que não está ali, diga que solicitará ajuda de um humano. Seja calorosa, empática, e use de 1 a 2 frases curtas."
    )
    
    final_prompt = (
        f"HISTÓRICO RECENTE COM ESTE CONTATO:\n"
        f"[(Início do Histórico)]\n"
        f"{history_str}\n"
        f"[(Fim do Histórico)]\n\n"
        f"NOVA MENSAGEM DO PACIENTE PARA VOCÊ RESPONDER AGORA: '{text}'"
    )
    
    # 4. INVOCAÇAO DA FACTORY (Complex ou Simple)
    # Como esta função representa o cérebro principal, requer mais QI (Complex)
    resposta = LLMFactory.generate(
        prompt=final_prompt,
        task_level="complex",  # Vai puxar DEFAULT_COMPLEX_MODEL do .env (gemini-2.5-pro / etc)
        system_instruction=system_prompt,
        temperature=0.5
    )
    
    return resposta

import os
import logging

logger = logging.getLogger(__name__)

class KnowledgeManager:
    """
    RAG Simples (MVP de Base de Conhecimento). 
    Lê todos os arquivos .md e .txt na pasta 'knowledge_base' e consolida
    em um bloco de contexto focado para injetar na Inteligência Artificial.
    
    Assim, basta a secretária, dono ou desenvolvedor jogar um texto novo lá dentro
    (Preços, Regras, Tratamentos Novos), para que a IA passe a "saber" de tudo 
    em tempo real instantaneamente, sem necessitar de banco de dados SQL ou Vetorial complexo.
    """
    
    # Aponta para a pasta /server/knowledge_base
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
    
    @classmethod
    def get_full_context(cls) -> str:
        """
        Varre a pasta de arquivos estáticos, concatena tudo e devolve para 
        ser usado como contexto absolutista na tomada de decisão da IA.
        """
        # Cria a pasta e o guia inicial caso o user (você) não tenha criado ainda.
        if not os.path.exists(cls.BASE_DIR):
            try:
                os.makedirs(cls.BASE_DIR, exist_ok=True)
                exemplo_path = os.path.join(cls.BASE_DIR, "1_regras_gerais.md")
                with open(exemplo_path, "w", encoding="utf-8") as f:
                    f.write("# Regras da MoveMind Clínica\nEdite este arquivo com os dados da empresa. Tudo que estiver aqui a IA vai dominar e responder aos clientes.\n\n- Horário de Funcionamento: Seg a Sex das 08h às 18h.\n- Endereço: Av. Paulista, 1000 - SP\n- Dr. Responsável: Breno\n")
            except Exception as e:
                logger.error(f"Erro ao criar estrutura do Knowledge MVP: {e}")
                return ""
            
        context_parts = []
        try:
            arquivos = sorted(os.listdir(cls.BASE_DIR)) # Ordem alfabética (1_, 2_)
            for filename in arquivos:
                if filename.endswith(".txt") or filename.endswith(".md"):
                    filepath = os.path.join(cls.BASE_DIR, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            context_parts.append(f"📄 [ARQUIVO: {filename}]\n{content}\n")
            
            if not context_parts:
                return "Nenhuma regra de negócio definida pela clínica."
                
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"❌ [KNOWLEDGE MVP] Falha ao ler base de textos: {e}")
            return "Erro ao carregar base de conhecimento interna."

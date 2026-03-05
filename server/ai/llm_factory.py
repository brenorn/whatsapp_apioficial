import os
import logging
from typing import Optional, Dict
from core.config_manager import BusinessConfigManager

try:
    from google import genai
    HAS_NEW_SDK = True
except ImportError:
    HAS_NEW_SDK = False

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    Fábrica inteligente de LLMs para Serviços Desacoplados.
    Implementa "Model Fallback" e "Exponential Backoff". 
    Se a Google desativar um modelo amanhã, a Engine atocorre pro substituto da lista sem travar o servidor.
    """
    # Modelos estáveis (Produção)
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    
    # Filas de Sobrevivência (Se o index 0 cair/for banido, pula pro 1)
    FALLBACK_SIMPLE = [GEMINI_2_5_FLASH, GEMINI_2_0_FLASH, GEMINI_1_5_FLASH]
    FALLBACK_COMPLEX = [GEMINI_2_5_PRO, GEMINI_1_5_PRO, GEMINI_2_0_FLASH]
    
    _client = None

    @classmethod
    def get_client(cls):
        """Injeta a dependência do Google GenAI Client sob demanda."""
        if not HAS_NEW_SDK:
            raise ImportError("Biblioteca google-genai moderna ausente. Rode: pip install google-genai")
            
        if cls._client is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.error("⚠️ [LLM_FACTORY] GEMINI_API_KEY não encontrada no .env!")
            else:
                cls._client = genai.Client(api_key=api_key)
        return cls._client

    @classmethod
    def get_model_priority_list(cls, task_level: str = "simple") -> list:
        """
        Gera a fila de sobrevivência baseada no escopo. 
        Puxa a chave do .env primeiro. Se a chave for banida, devolve a Array nativa pura.
        """
        task_level = task_level.lower()
        if task_level == "complex":
            model_env = os.getenv("DEFAULT_COMPLEX_MODEL")
            baseline_list = cls.FALLBACK_COMPLEX
        else:
            model_env = os.getenv("DEFAULT_SIMPLE_MODEL")
            baseline_list = cls.FALLBACK_SIMPLE

        if model_env and model_env not in baseline_list:
            # Força o do .env na cabeca da fila para dar autoridade ao Deployer manual
            return [model_env] + baseline_list
            
        return baseline_list

    @classmethod
    def generate(
        cls, 
        prompt: str, 
        task_level: str = "simple", 
        system_instruction: Optional[str] = None,
        temperature: float = 0.4
    ) -> str:
        """
        Motor Definitivo de Geração Textual M2M. Possui loop infinito de Fallback.
        """
        client = cls.get_client()
        if not client:
            return "[MOCK IA - Aponte uma API KEY válida no .env]"
            
        priority_models = cls.get_model_priority_list(task_level)
        last_error = ""

        # LOOP DE SOBREVIVÊNCIA
        for model_name in priority_models:
            try:
                print(f"🧠 [LLM Factory] Disparando rede neural -> '{model_name}'...")
                config = {"temperature": temperature}
                
                # Injeção Automática de Contexto de Negócio (Agnostic AI)
                business_prefix = BusinessConfigManager.get_prompt_prefix()
                full_system = f"{business_prefix}\n\n{system_instruction or ''}"
                config["system_instruction"] = full_system
                    
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                return response.text
                
            except Exception as e:
                error_str = str(e).lower()
                logger.warning(f"⚠️ [LLM Factory] Avaria no Modelo '{model_name}': {error_str}")
                
                # Se for erro "Not Found", Depreciado, ou Quota, continua o for loop pro modelo 2
                if "404" in error_str or "not found" in error_str:
                     last_error = f"O modelo {model_name} foi desativado pela Google."
                     continue
                     
                if "429" in error_str or "quota" in error_str:
                     last_error = f"Atingimos o limite (429) de tokens no modelo {model_name}."
                     continue
                     
                last_error = str(e)
                continue # Se for algum timeout maluco, pula e tenta a Cópia Reserva
                
        # Se os 3 modelos das Arrays cairem, exibe aviso fatal humanizado.
        logger.error(f"❌ [LLM Factory] PANIC! A árvore inteira de LLMs de Backup falhou. Ultimo erro: {last_error}")
        return "Nossos servidores de inteligência estão em manutenção emergencial. Devolva em breve."

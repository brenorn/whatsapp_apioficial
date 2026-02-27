# 🤖 Arquitetura Baseada em Agentes (CrewAI-Style) para o WhatsApp API
> **Inspiração:** Análise profunda da engenharia do repositório `move_git/backend/ai_engine/src/domains/nr1`.
> **Objetivo:** Adotar o padrão declarativo `.yaml` (YAML-Driven Configuration) para orquestrar os microsserviços do WhatsApp (Acessibilidade, Vendas, Retenção e Agendamento), garantindo acoplamento frouxo, extrema escalabilidade (BMAD) e isolamento de papeis.

---

## 🏗️ 1. O Paradigma de Orquestração Declarativa (Inspirado no NR-01 Engine)

No projeto NR-1, observou-se que a Inteligência Artificial não atua como uma "caixa preta única". Ela foi dividida cirurgicamente em *Personas* (Agentes) e *Etapas de Trabalho* (Tasks), tudo definido via arquivos estáveis `.yaml`.
Isso nos ensina algo valioso: **Não devemos hardcodar prompts dentro das lógicas de API do WhatsApp.**

### A Grande Vantagem do Padrão YAML (Design Pattern: Strategy/Observer)
1. **Separação de Preocupações (SoC):** O desenvolvedor backend (Python/FastAPI) programa apenas a fiação dos dados. O Engenheiro de Prompt mexe apenas nos YAMLs.
2. **Modularidade CrewAI:** Cada agente possui nome, *backstory* (história de fundo), meta e *tools* (ferramentas).
3. **Escalão de IA:** Se pedirmos para o bot agendar, não usamos o cérebro caro inteiro. Chamamos especificamente o `Agente Recepcionista`. Se for fechamento de PIX, chamamos o `Agente Financeiro`.

---

## 📂 2. Árvore de Diretórios Sugerida (Aplicando ao Módulo WhatsApp)

Vamos reconstruir a governança do cérebro na pasta `server/ai` para suportar os 5 Microsserviços futuros. A estrutura será:

```text
server/
 └── ai/
     ├── config/
     │   ├── agents.yaml      # Definição das Personas (Recepcionista, Curador, Transcritor)
     │   ├── tasks.yaml       # Ordens de Trabalho (Flows, STT, CAPI)
     │   └── tools.yaml       # Ferramentas q os agentes podem invocar (Ex: check_calendar)
     ├── agent_factory.py     # Lê os YAMLs e instancia as sinapses (Gemini/Langchain)
     ├── task_orchestrator.py # Cria o pipeline (Ex: Áudio -> Transcritor -> Recepcionista)
     └── audio_processor.py   # Usa o Agente Transcritor
```

---

## 📝 3. Estruturação Técnica: Como os arquivos YAML ficarão

### 3.1. `ai/config/agents.yaml` (As Personas de Conversão)
Aqui nós damos vida, cargo e restrições legais (LGPD) a cada rede neural do boilerplate.

```yaml
# 🧠 Agentes do Ecossistema Clínico (Máquina de Vendas)

clinical_receptionist:
  name: "Recepcionista Consultiva Sênior"
  role: "Triagem e Conversão Primária Inbound"
  backstory: >
    Você é a primeira voz da clínica. Especialista em empatia e gatilhos mentais. 
    Seu foco não é dar diagnóstico médico, mas entender a dor superficial e 
    conduzir o paciente para o fluxo de Agendamento (Flows) ou Venda (Catálogo).
  goal: "Converter dúvidas em ativação do Microsserviço de Fechamento."
  model: "gemini-1.5-flash"

audio_transcriptor:
  name: "Perito Transcritor STT (Speech-To-Text)"
  role: "Acessibilidade e Decodificação de Áudio"
  backstory: >
    Você atua nos bastidores. Recebe gravações de pacientes relatando sintomas gagos,
    nervosos ou em barulho. Você aplica rigor ortográfico e termos técnicos da OMS.
  goal: "Transformar áudio caótico em JSON/String perfeito para a Recepcionista."
  model: "gemini-1.5-flash-8b"

retention_specialist:
  name: "Estrategista de Recaptura (Broadcast)"
  role: "Recuperação de Carrinhos e Leads Frios"
  backstory: >
    Você analisa as objeções do por que o PIX não foi pago em 2 horas. 
    Formula textos persuasivos curtos usando o princípio da Urgência e Escassez.
  goal: "Gerar os textos dos templates Meta pré-aprovados elevando ROI em 45%."
  model: "gemini-1.5-pro"
```

### 3.2. `ai/config/tasks.yaml` (As Fichas de Trabalho)
Cada microsserviço (Projeto 1, 2, 3...) é engatilhado por uma "Task" oficial. Se o Orquestrador detectar Áudio, ele não chama a IA, ele manda a Ordem de Serviço "transcribe_patient_audio".

```yaml
# 📋 Tarefas Orquestradas do Backend

transcribe_patient_audio:
  name: "Processamento de Áudio e Acessibilidade"
  description: >
    O Perito Transcritor recebe o OGG binário via GCS. 
    Retorna a string higienizada sem falhas. 
    Saída: String pura (Para injetar nas memórias do Chat).
  agent: "audio_transcriptor"
  expected_output: "Texto perfeitamente legível."

abandoned_cart_recovery:
  name: "Disparo de Urgência (Pós-Dropout de 2h)"
  description: >
    O Estrategista lê a soma financeira (R$ 350,00) que o OrderProcessor gerou 
    no banco de dados. Elabora a frase para convencer o paciente a quitar o PIX agora.
  agent: "retention_specialist"
  expected_output: "Template Meta formatado com variáveis."
```

---

## 🚀 4. A Execução na Python Engine (DMAIC + BMAD)

Como conectamos isso no código real que escrevemos hoje (ex: o Orquestrador)?
Usamos uma `AgentFactory` (Idêntico ao `drps_generator.py` do projeto NR01).

```python
# Em server/ai/task_orchestrator.py
from utils.yaml_reader import load_yaml
from config.llm_settings import GeminiClient

class CrewOrchestrator:
    def __init__(self):
        self.agents = load_yaml("ai/config/agents.yaml")
        self.tasks = load_yaml("ai/config/tasks.yaml")

    def execute_audio_task(self, audio_binary):
        # 1. Carrega persona (Context/System Instruction)
        agent_profile = self.agents["audio_transcriptor"]
        
        # 2. Configura a Segurança Cibernética (System Prompt Blindado)
        system_instruction = f"Você é {agent_profile['name']}. {agent_profile['backstory']}"
        
        # 3. Invoca o Modelo EXATO requisitado no YAML (Controle de Custos BMAD)
        # Ex: gemini-1.5-flash-8b (Custa centavos) vs Pro (Custa reais)
        result = GeminiClient.generate(
            model=agent_profile['model'],
            instructions=system_instruction,
            contents=[audio_binary, self.tasks['transcribe_patient_audio']['description']]
        )
        return result.text
```

### 🎯 Benefícios Diretos Desta Refatoração (Por que fazer isso?)
1. **Mudança Rápida:** O Dono da Clínica diz: *"Achei a recepcionista muito seca"*. Você não perde tempo caçando `main_brain.py` e recompilando servidores. Você abre o `agents.yaml`, altera o `backstory` e o sistema puxa ao vivo a nova personalidade.
2. **Isolamento de Erro:** Se a Recaptura (Broadcast) alucinar, sabemos que o problema foi no `retention_specialist`, e a agenda/venda normal da clínica segue faturando.
3. **Padrão Ouro Internacional:** Isso coloca a sua arquitetura ao lado dos padrões massivos usados pelo *LangChain* e *CrewAI*, mas com performance nativa usando Google Gemini Direto (zero overhead das bibliotecas pesadas).

# 🏗️ Planejamento Estratégico de Microsserviços (Fase 2 a 5)
> **Metodologia Aplicada:** BMAD (Business, Marketing, Architecture & Design) + DMAIC (Six Sigma)
> **Foco:** Segurança Cibernética, Escalabilidade Absoluta e Eficácia (Design Patterns).

Este documento detalha o planejamento cirúrgico e a engenharia de software reversa para a implementação dos próximos 4 microsserviços do ecosistema WhatsApp. A arquitetura foi desenhada para suportar milhões de requisições concorrentes ("Enterprise-grade") sem ferir a Lei Geral de Proteção de Dados (LGPD/GDPR) nem comprometer a resiliência do core.

---

## 🎙️ PROJETO 2: STT Audio Workflow (Fim dos Áudios não Lidos)
**Caminho do Arquivo:** `server/ai/audio_processor.py`

### 1. Metodologia DMAIC
* **Define (Definir):** Clínica perde 40% dos agendamentos pois a IA não ouve áudios relatando sintomas longos.
* **Measure (Medir):** Quantidade de webhooks com `msg_type == "audio"` com drop (abandono) na sessão atual. Mensurar o delay da nuvem.
* **Analyze (Analisar):** O WhatsApp envia um `media_id`. Baixar o áudio dura ~1.5s, rodar no Whisper local quebra a RAM, usar API do Gemini Flash dura 0.8s.
* **Improve (Melhorar):** Injetar o texto gerado de volta no Pipeline do NLP principal, enganando a camada superior dizendo que foi "texto".
* **Control (Controlar):** Excluir o binário `.ogg` da pasta `temp/` em FileSystem após 2 segundos (Data Privacy / LGPD).

### 2. Metodologia BMAD & Segurança
* **Business:** Zero objeção. Atende inclusão digital (idosos preferem áudio).
* **Architecture (Design Patterns):** **Adapter Pattern**. A interface do `Main Brain` só entende Strings. O `AudioProcessor` atua como um Adaptador Universal traduzindo Binário para String antes de acionar a lógica de negócios.
* **Cybersecurity:** Os áudios dos pacientes NUNCA serão salvos em banco de dados ou buckets sem criptografia "em repouso". Após usar o binário na API STT (Speech-to-Text) com SSL (TLS 1.3), aplicar exclusão profunda (`os.unlink`).

---

## 📝 PROJETO 3: Flows Manager (A Agenda In-App)
**Caminho do Arquivo:** `server/experience/flows_manager.py`

### 1. Metodologia DMAIC
* **Define:** Pacientes demoram 15 minutos trocando mensagens para fechar uma agenda (ex: *"e terça?", "tem as 14h?", "não posso"*). 
* **Measure:** Tempo médio de conversação por agendamento (Tempo de Resolução - TTR).
* **Analyze:** O *WhatsApp Flows* reduz o TTR em 85%. A tela mostra os dias disponíveis direto numa User Interface (UI) limpa.
* **Improve:** Substituir LLM Consultivo por *Form Processing*. O webhook envia payload validado via JSON criptografado.
* **Control:** Assinatura ECDSA nos payloads. O WhatsApp assina criptograficamente o Formulário recebido para impedir Man-In-The-Middle attack de dados de saúde.

### 2. Metodologia BMAD & Segurança
* **Design/Marketing:** O Layout do Flow (JSON) usará botões ergonômicos e tipografia da própria clínica para elevar a autoridade (Branding).
* **Architecture (Design Patterns):** **Facade Pattern**. O `FlowsManager` oculta a terrível complexidade do envio de "Mensagens Interativas JSON" da Meta, exportando apenas o comando simples `trigger_schedule_flow(phone)`.
* **Cybersecurity:** Validar a assinatura de chave pública do Form (Endpoint da Meta Decrypt) usando chaves AES-256 GCM antes de jogar o agendamento no banco de dados para prevenir "Spoofing" de dados.

---

## 📊  PROJETO 4: CAPI Tracker Integrator (Marketing Hub da Meta)
**Caminho do Arquivo:** `server/marketing/capi_tracker.py`

### 1. Metodologia DMAIC
* **Define:** A clínica gasta R$ 10.000,00 no Facebook Ads, a venda ocorre solta no WhatsApp (via PIX - Projeto 1), e o Gerenciador de Anúncios pensa que o custo por aquisição foi zero. Falsa métrica de ROI.
* **Measure:** Perda de "Event Match Quality" (EMQ) nos anúncios.
* **Analyze:** Capturar o `fbclid` ou `wa_id` inicial e mapear com hashs SHA-256 exigidos pelo protocolo CAPI (Conversions API).
* **Improve:** Quando `OrderProcessor` assinalar "Pago", chamar `capi_tracker`.
* **Control:** Enfileirar as conversões (Message Broker/Redis) para reenviar caso a Meta Network sofra TimeOut de resposta em Black Friday.

### 2. Metodologia BMAD & Segurança
* **Marketing:** Treinamento de Algoritmo de Lances. Diminuição exponencial de CAC (Custo de Aquisição de Cliente) mostrando pra IA do Facebook o "perfil exato" de quem compra via Zap.
* **Architecture (Design Patterns):** **Observer Pattern**. O `CAPI Tracker` fica "ouvindo" o sistema de pagamentos de forma totalmente desacoplada. Se o CAPI cair, as vendas continuam normais.
* **Cybersecurity:** LGPD Obrigatório. Nunca enviar Nomes Claros nem Celulares brutos. Enviar exclusivamente strings anonimizadas com via um processo de **Hash Criptográfico Duplo (SHA-256)** conforme contrato do Facebook Data Processing Terms.

---

## 🧲 PROJETO 5: Recaptura & Broadcast Engine (Pós-Venda Ativo)
**Caminho do Arquivo:** `server/marketing/broadcast_engine.py`

### 1. Metodologia DMAIC
* **Define:** Carrinhos gerados pelo Projeto 1 e não pagos perdem-se no esquecimento.
* **Measure:** Taxa de conversão por Carrinho (Atualmente em 30%). O restante é "Drop" (Desistência de 70%).
* **Analyze:** A intervenção dentro de até 2 a 4 horas com uma oferta utilitária recupera até 45% desse Drop.
* **Improve:** Implementar um loop ou Job (Cron Jobs/Celery) varrendo `whatsapp_messages` onde status for `pending_pix` após 120 minutos.
* **Control:** Teto de vidro comercial: Colocar trava booleana `has_been_notified_drop = True` no banco de forma atômica para impedir que a Clínica faça Spam de cobrança (Risco de bloqueio do WhatsApp Oficial).

### 2. Metodologia BMAD & Segurança
* **Business:** Uma Feature que é uma verdadeira copiadora de dinheiro (Re-Sales automáticos de base quente).
* **Architecture (Design Patterns):** **Strategy & Batch Pattern**. Recuperar não apenas com um template fixo. Agrupar disparos a cada 100 mensagens (Batches) para não causar negação de serviço (`DDOS` na própria API) nem bater no limit rate do Facebook Cloud (Atualmente em 80 mensagens/segundo para Tier 1).
* **Cybersecurity (LGPD - Opt-out):** Todos os Templates disparados de forma Proativa pelo Broadcast devem conter o botão "Interactive Button" de Opt-out ("Parar de receber Promoções"). Se clicado, rotula o usuário na Blacklist de marketing instantaneamente (Database Nível Row Lock).

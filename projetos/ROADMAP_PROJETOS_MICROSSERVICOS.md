# 🏗️ ESCOPO DE ENGENHARIA E PROJETOS: 5 MICROSSERVIÇOS GLOBAIS
> Documento-Guia de divisão e construção por estágios independentes do Boilerplate WhatsApp-Commerce 2026.

Entendido o pedido. Para não misturarmos módulos que impactem a produção uns dos outros (Monolito), definimos que faremos "O Sistema Fatiado" em 5 Projetos Completos e independentes. A adoção por Microsserviços nos permite plugar e testar as features uma por vez.

Abaixo está a planta de cada um dos Projetos (Módulos). Concluímos o **Projeto 1** e os próximos serão tratados em Sprint.

---

## 🟢 PROJETO 1 [CONCLUÍDO]: Payment Gateway e Máquina de Carrinhos
**Objetivo:** Permitir checkout 100% autônomo e sem humanos, faturando direto no chat via PIX emulando um Banco as a Service.
*   **Pastas Criadas:** `server/commerce/`
*   **Classes Implantadas:** `PaymentGateway` (.py), `CatalogManager` (.py), `OrderProcessor` (.py).
*   **Conexões feitas:** O `Orquestrador` agora corta a falação do chatbot de IA toda vez que recebe um JSON Webhook com o `msg_type == "order"`. E cospe devolta o Linha Digitável e BR Code em tempo intercional do WhatsApp.
*   **Ready to Prod?** Sim. Depende apenas que o Administrador preencha a chave **PIX_DICT_KEY** no aquivo `.env` do servidor.

---

## 🟢 PROJETO 2 [CONCLUÍDO]: STT Audio Workflow (Fim dos Áudios não Lidos)
**Objetivo:** Acessibilidade e Conversão. Transformar áudios gigantes em pacotes JSON transacionáveis e injetá-los direto no Cérebro principal (RAG) para que não precisemos da secretária.
*   **Microsserviço-Alvo:** `server/ai/audio_processor.py`
*   **Como foi construído:** Usamos a API da META para gerar a URL (método `download_media` desenvolvido no cloud_client). Baixamos o `.ogg`. O Google Gemini (Modelo `gemini-1.5-flash-8b`) entra, faz OCR, transcreve o áudio com vírgulas e depois aplicamos "Zero-Retention" excluindo permanentemente o áudio do HD em proteção à LGPD.
*   **Impacto no Orquestrador:** Ele intercepta o evento, reescreve a `log_message` com a tag `🎙️ [Transcrevi o áudio recebido]` e devolve a versão textual na memória para a IA Principal responder.

---

## 📝 PROJETO 3: Flows Manager (A Agenda Nativa In-App)
**Objetivo:** Permitir que leads respondam formulários completos pelo chat usando Dropdowns e Datapickers, como miniapplicativos Meta Web.
*   **Microsserviço-Alvo:** `server/experience/flows_manager.py`
*   **A Rota:** O bot nunca mais vai dizer: "Qual a data da agenda?", "Qual o horário?", "Por favor escreva". Ele emitirá `cloud_api.send_interactive_flows(flow_id)`. O WhatsApp do cliente travará a tela inteira com as disponibilidades puxadas do calendário da Clínica. Se fechou, o Hook devolve pra IA.

---

## 📊  PROJETO 4: CAPI Tracker Integrator (Marketing Hub)
**Objetivo:** Devolver resultados tangíveis de Inteligência de Tráfego Orgânico/Meta Ads pra equipe Comercial (Atribuição do PIX faturado).
*   **Microsserviço-Alvo:** `server/marketing/capi_tracker.py`
*   **A Rota:** Iremos escutar a primeira viajem do Lead (Usando o Click ID escondido na url do Zap - fbclid). Tão logo o *Projeto 1 (Payment Gateway)* confirme PIX Ganhado, o Tracker varre a string de HTTP em modo background (`BackgroundTasks`) informando o Meta Business Manager Oficial: "1 Conversão de 350 Reais do Lead C_2X foi efetuada", retroalimentando machine-learning dos Anúncios.

---

##  🧲 PROJETO 5: Recaptura de Oportunidades & Broadcast
**Objetivo:** Re-acender base fria sem estourar limites Meta. Automações Pós-Abandono.
*   **Microsserviço-Alvo:** `server/marketing/broadcast_engine.py` e `cron_abandoned.py`
*   **A Rota:** Iremos injetar bibliotecas Assíncronas que monitoram a timestamp do DB. Carrinhos sem movimentação passam por um check na aba `status` do Postgre após 2 horas de `pending`. Uma trigger devolve uma mensagem templar via Template ID Ouro da Meta (R$ 0,38 para Marketing) ofertando "Termine sua compra por R$ 330 com desconto exclusivo de 2h".

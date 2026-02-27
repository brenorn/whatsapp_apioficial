# 🛒 Documentação Oficial: Máquina de Vendas (Commerce Engine)
**Versão:** 1.0 (Integração Nível Enterprise)
**Escopo do Microsserviço:** Vendas Nativas In-App (Catálogo, Carrinho e Interações) via Meta Cloud API Oficial.

---

## 🎯 1. Visão Geral (Por que este módulo existe?)
O objetivo do **Commerce Engine** é transformar o *WhatsApp Boilerplate* de uma ferramenta puramente "Consultiva" (onde a IA tira dúvidas) para uma ferramenta **"Transacional"** (onde a clínica/empresa realiza a venda e recebe o dinheiro diretamente dentro do chat do paciente).

Este microsserviço é isolado da IA Principal para garantir que cálculos financeiros (soma do carrinho, descontos, geração de PIX) não sofram **"Alucinações de LLM"**. A Inteligência Artificial foca em ser humana, persuasiva e empática; o Commerce Engine foca em ser matemático, lógico e seguro.

---

## 🧩 2. Arquitetura e Componentes Atuais
A arquitetura de vendas está alocada dentro da pasta `server/commerce/` e estendeu os módulos de comunicação:

### 📦 2.1. O Parser Transacional (`core/webhook_parser.py`)
Não ignoramos mais as vendas. Quando um paciente navega pelo catálogo do WhatsApp e clica em **"Enviar Carrinho"**, a Meta dispara um webhook JSON gigantesco.
* **O que ele faz:** O Webhook Parser intercepta a requisição, detecta que o `msg_type` é `"order"` (e não `"text"`) e empacota a variável blindada `order_data`.

### 🚦 2.2. O Interceptador (`core/orchestrator.py`)
A *Golden Rule* das vendas: Carrinhos de compra não devem gastar dinheiro de chamadas de IA.
* **O que ele faz:** Antes de ativar as Sinapses do Gemini (Main Brain), o orquestrador verifica a tag. Se for um carrinho, ele **aborta a IA** e envia os dados limpinhos direto para o `OrderProcessor`.

### 🧮 2.3. O Processador de Pedidos (`commerce/order_processor.py`)
O coração matemático do checkout.
* **O que ele faz:** Recebe o `order_data`, lê a lista de itens (`product_items`), enxerga as quantidades, as moedas locais (`currency`) e soma o total da fatura. Devolve imediatamente para o orquestrador um JSON formatado liberando o WhatsApp a responder *"Recebemos seu carrinho no valor de R$ X"*.

### 🏬 2.4. O Gerente de Catálogo (`commerce/catalog_manager.py`)
O sistema de "Estoque e Vitrine". 
* **O que ele faz:** Possui a capacidade de bater na `Graph API` usando o seu Token e consultar tudo que você conectou lá na Nuvem do Facebook (Preços Mágicos e Títulos dos Tratamentos). No futuro, a IA RAG consultará este arquivo para responder aos leads *"Sim, temos este produto em estoque e custa R$ X"*.

### 📱 2.5. Disparos Sensoriais (`core/whatsapp_cloud_client.py`)
A biblioteca que fala com a Meta aprendeu 2 novos golpes cruciais de persuasão:
1. `send_interactive_buttons`: Envia mensagens não-textuais (Botões formatados).
2. `send_product_message`: Envia um Card Visual deslumbrante puxando a foto e preço de um ID do seu Commerce Manager, liberando o botão In-App "Adicionar ao Carrinho".

---

## 🌊 3. Fluxo de Vida de uma Compra (O Funil Ideal)

Se um desenvolvedor quiser plugar este fluxo completo, esta é a vida orgânica do código rodando:

1. **Lead Reclama:** "Quero agendar algo mas não sei o que." -> (`manage_incoming_message` -> `generate_ai_response`).
2. **IA Atua:** O Brain consulta a clínica e decide que o "Peeling" é ideal. O Brain diz para o Developer: "Ative a Vitrine do Peeling".
3. **Vitrine Pula (Trigger):** O Dev usa o método `cloud_api.send_product_message(phone, catalogo_id, produto_peeling_id)`. O WhatsApp mostra o produto.
4. **Lead Comprando:** O Lead aperta em "Adicionar" e clica num ícone verde no Zap "Mandar Pedido para o Bot".
5. **A Mágica:** Webhook cai -> Parser grita `"order"` -> Orquestrador desliga o AI -> OrderProcessor gera a soma do recibo (350 reais) -> Responde para pagar o PIX.

---

## 🛠️ 4. O Que já está FEITO e PRONTO (Status Atual)
✔️ Interceptação do Carrinho (Ignorar Custo e Rota de IA).
✔️ Extração blindada do Preço, Moeda, Qtde de Itens e Retailer IDs do produto.
✔️ Função pronta para enviar Botões Nativos.
✔️ Função pronta para enviar Produto da Vitrine.
✔️ Conector estruturado para consultar o Catálogo da Meta via Graph API.

---

## 🚀 5. ROADMAP: O Que PODE (e DEVE) ser Feito (Para Desenvolvedores)

Se a sua clínica/empresa quiser ativar faturamento na veia através de programadores terceiros ou em sprints futuras, **coloque estas 4 Tarefas no Board**:

### 🎯 Tarefa 1: Geração Dinâmica de Pix (Gateway de Pagamento) [CONCLUÍDO✔️]
**Onde atuamos:** Criamos o arquivo `commerce/payment_gateway.py`.
**A Ação:** O `OrderProcessor` agora chama `PaymentGateway.generate_pix_charge()` no momento exato em que finaliza a soma dos valores do carrinho. O sistema retorna instantaneamente o "Texto Copia e Cola" (BR Code) e o link do QR Code da API externa, blindando os cálculos contra alucinações da IA.

### 🎯 Tarefa 2: Retenção e Abandono de Carrinho
**Onde atuar:** Adicionar um agendador Celery ou APScheduler.
**A Ação:** O `OrderProcessor` grava no banco de dados Postgres: A ordem `O-123` tem o `status = 'pending_payment'`. Um script Python roda de 20 em 20 minutos. Se a ordem não foi paga há mais de 2 horas, dispara a campanha limitadíssima da Meta de Abandono (`template_abandonment`) oferecendo 10% de Desconto automático. Retorno sob investimento brutal.

### 🎯 Tarefa 3: Sincronização de Banco (SSOT - Single Source of Truth)
**Onde atuar:** `commerce/catalog_manager.py`.
**A Ação:** A API de catálogo hoje "só pega" os produtos. Um desenvolvedor pleno pode codar o Endpoint de "Update" usando Meta Batch API. Se a atendente mudar o preço da Consulta de R$ 500 para R$ 150 no painel da Vercel, o Python injeta na veia da Meta a alteração quase em tempo real, impedindo que o WhatsApp exiba preço errado aos pacientes.

### 🎯 Tarefa 4: O Botão Nível 0 (Menu Interativo)
**Onde atuar:** O `main.py` disparador M2M.
**A Ação:** Quando um Lead bater ponto a primeira vez no bot e não quiser escrever nada, disparar a mensagem nativa "Reply Buttons". *[ Falar Com Atendente ] [ Ver Tratamentos ]*. Isso reduz atrito cognitivo em 80%. O Parser já está desenhado para ler a resposta de botões interativos nas regras lançadas hoje.

---

**Equipe de Desenvolvimento | Padrões:**
*Não apagar nem remover Pydantics. Não permitir que APIs GenAI gerem valores monetários calculados à mão. Somente o OrderProcessor detém autoridade financeira do microsserviço.*

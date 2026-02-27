# 🛒 Projeto: Máquina de Vendas no WhatsApp (Commerce Engine)
> **Estudo Arquitetural e Roadmap de Implementação de E-commerce Nativo**

Este documento mapeia os recursos oficiais da Meta Graph API voltados para transações financeiras e como podemos acoplar um **novo microsserviço de vendas** ao nosso Boilerplate atual, transformando o bot de um "Atendente de Clínica" em um E-commerce de alta conversão.

---

## 1. 🛍️ O Que a "WhatsApp Business API" Oferece Nativamente para Vendas?
A Meta lançou recentemente recursos que eliminam a necessidade de mandar o cliente para um "Link de Site Externo". Toda a jornada (ver catálogo, adicionar ao carrinho e pagar) acontece dentro do chat.

### A) Mensagens Interativas (A Isca)
Em vez de texto corrido, podemos usar APIs do tipo `interactive`. Elas convertem 3x mais pois o usuário clica ao invés de digitar:
*   **List Messages:** Um menu que abre com até 10 opções (Ideal para "Mostrar Categorias de Produtos" ou "Serviços da Clínica").
*   **Reply Buttons:** Até 3 botões embutidos na mensagem (Ideal para "Comprar Agora", "Falar com Vendedor").

### B) Catálogos e Produtos Formatos (A Vitrine)
O WhatsApp permite ligar o seu ID a um Catálogo (Meta Commerce Manager).
*   **Single Product Message (PDP):** Você chama a API passando o ID de um produto específico (Ex: "Sessão de Terapia") e ele plota um balão bonito com Foto, Título, Preço e o botão "Ver Produto".
*   **Multi-Product Message:** Você manda uma "estante" com até 30 produtos divididos em sessões.

### C) Carrinho de Compras e Order Payload (O Checkout)
Quando o cliente clica nos produtos enviados e aperta em "Adicionar ao Carrinho" no próprio app do Whatsapp, ele não vai para site nenhum. Ele clica num ícone verde de carrinho no topo do App e manda para o seu provedor.
* **Webhook de Ordem:** O nosso webhook (que blindamos antes) vai receber não um tipo `text`, mas um tipo `order`. Esse JSON já vem com o ID de tudo que ele escolheu, quantidade e o valor final.

### D) Pagamento Nativo (O Fechamento)
No Brasil, a API Oficial do WhatsApp suporta fluxos integrados com Cielo, Mercado Pago e PagSeguro para o cliente colocar o cartão de crédito SEM sair do Whatsapp, ou fazer o PIX lendo QR Code.

---

## 2. 🧩 Desenho do Novo Microsserviço de Vendas

Para não destruir a nossa arquitetura atual (que é excelente para atendimento), não colocaremos regras de vendas misturadas no `main_brain.py`. Construiremos uma pipeline híbrida chamada **Commerce Engine**.

### 📦 A Nova Estrutura de Pastas
```text
server/
  ├── ai/
  │    ├── main_brain.py        (Conversa e Secretária)
  │    └── checkout_brain.py    (NOVO: Especialista em Persuasão e UpSell)
  ├── commerce/
  │    ├── catalog_manager.py   (NOVO: Conecta com a Vitrine da Meta)
  │    ├── order_processor.py   (NOVO: Intercepta o Carrinho e Gera o Link de Pgto)
  │    └── payment_gateway.py   (NOVO: Verifica se o PIX/Cartão foi pago)
  └── core/
       └── webhook_parser.py    (ATUALIZADO: Aprende a ler msg do tipo "order")
```

---

## 3. 🛣️ Como a IA (Gemini) e a Engenharia Vão Agir Juntas? (Fluxo de Trabalho)

O mercado mundial separa chatbots entre **Consultivos (IA)** e **Transacionais (Menus Nativos)**. Juntar os dois é a bala de prata.

**Passo 1: Descoberta (LLMFactory -> Complex)**
* **Lead:** *"Quero um tratamento para manchas no rosto."*
* **IA do Cérebro:** O Gemini analisa o intent, busca na base (RAG) e responde de forma humana: *"Nós temos o protocolo Peeling X, que é excelente para isso!"*

**Passo 2: Apresentação (Catalog Manager -> Meta Cloud Client)**
*   A IA emite um gatilho interno para o código: `[TRIGGER_PRODUCT_123]`
*   O nosso orquestrador lê o gatilho, ignora a resposta visual suja, e invoca o `WhatsAppCloudClient.send_product_message("123")`.
*   O Lead recebe um Card lindo do Whatsapp com a Foto do Tratamento e botão "Adicionar".

**Passo 3: A Conversão (Webhook Parser -> Order Processor)**
* O Lead envia o carrinho.
* Nosso Webhook Parser pega `msg_type == "order"`.
* O `manage_incoming_message` envia para o novo `order_processor.py`. 
* O processador lê: Tratamento Facial, Quantidade 1, Total: R$ 350. Gera o PIX e Devolve pra Meta nativamente!

**Passo 4: Pós-Venda (Handoff Automático)**
* O Webhook de confirmação de pagamento bate.
* O robô agradece, emite recibo em PDF (via Document Message) e atualiza o funil no seu Banco de Dados (Postgres).

---

## 4. 🥇 Como Garantir Padronização Mundial nesse Serviço?

Empresas como Zendesk, Hubspot e Salesforce seguem normas que devemos copiar para criar essa feature:

1. **Catálogo como Fonte da Verdade (SSOT):** Os produtos não podem nascer apenas no Banco de Dados. A API de Vendas Meta obriga o upload contínuo para o Gerenciador de Comércio do Facebook via API Sync.
2. **Abandono de Carrinho:** Um serviço (Celery Task) que aguarda 4 horas. Se o webhook do tipo `order` foi disparado mas nunca fechado com o PIX, a máquina dispara um modelo de msg ativa pre-aprovada `"Esqueceu alguma coisa? Temos 10% de desconto no seu checkout de R$ 350!"`.
3. **Sinalização Transacional Cautelosa:** O webhook deve sempre atualizar o `update_message_status()` do nosso banco, pois a confirmação de leitura (`read`) de um link de pagamento aumenta as chances de contato humano. Se leu e não pagou, manda o humano atuar.

### Próximos Passos
1. Atualizar o `webhook_parser.py` para não dar "Ignore" em tipos `interactive` e `order`.
2. Criar os novos arquivos na pasta `/commerce/`.
3. Adicionar as funções nativas de List, Button e Catalog na classe `whatsapp_cloud_client.py`.

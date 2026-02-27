# 💰 PROJETO 19: AI Sales Negotiator (V2.0)

> **Status:** Engenharia de Fechamento (Baseado em Chris Voss e LTV Dynamic Pricing)
> **Objetivo:** Maximizar a taxa de fechamento de orçamentos no WhatsApp, utilizando empatia tática para desarmar objeções e protegendo a margem de lucro através de decisões baseadas no valor vitalício do cliente (LTV).

---

## 🏗️ 1. O Conceito "Guardian of Margins"
O negociador comum cede no preço por medo de perder a venda. O **AI Negotiator** usa dados:
- **Empatia Tática:** Usa técnicas de negociação de reféns do FBI para criar conexão e autoridade.
- **Data-Driven Discount:** O nível de flexibilidade é proporcional ao LTV do cliente. Clientes fiéis ganham benefícios; novos leads ganham valor agregado.

---

## 🛠️ 2. Workflow de Negociação
1.  **Detecção de Objeção:** O cliente envia uma negativa ou hesitação (Ex: *"Vou pensar"*, *"Está caro"*, *"Tenho que falar com meu marido"*).
2.  **Labeling & Mirroring (IA):** O bot aplica um rótulo emocional: *"Parece que você está sentindo que este investimento não cabe no seu orçamento mensal agora?"*.
3.  **Análise de LTV (Projeto 8):** O bot verifica o histórico:
    - `High LTV`: Oferece cortesia ou parcelamento estendido.
    - `Low LTV`: Oferece urgência (Ex: *"Se fecharmos hoje, consigo [X]"*).
4.  **Calibrated Questions:** *"O que precisaríamos ajustar para que você se sinta 100% segura em começar seu tratamento hoje?"*.

---

## 💻 3. Layer de Decisão (Discount Matrix)
O bot segue regras de negócio rígidas para não quebrar a margem:
- **Regra 1:** Nunca comece com desconto. Comece reforçando o valor (ROI/Resultado).
- **Regra 2:** Se o desconto for inevitável, troque por algo em troca (Ex: *"Dou 5% se você pagar à vista ou me indicar 1 amigo"*).
- **Regra 3:** Bloqueio automático se o pedido de desconto ultrapassar o limite configurado em `margin_config.yaml`.

---

## 🧠 4. Prompt de Negociação (FBI Style)

```yaml
method: "Never Split the Difference"
techniques:
  - Mirroring: Repita as últimas 3 palavras do cliente em tom de dúvida.
  - Labeling: Nomeie as emoções negativas para que elas percam força.
  - No-Oriented Questions: Busque o 'Não' que significa proteção (Ex: 'Seria um erro considerar essa oferta?').
  - Summary: Reepilogar tudo o que o cliente disse para obter o 'That's Right'.
```

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 16 (Digital Twin)**. Se a negociação estiver "morna", o bot sugere: *"Deseja que eu gere um áudio personalizado do médico (com a voz dele) reforçando a importância clínica deste tratamento agora?"*. A autoridade do médico clonado costuma fechar a venda na hora.

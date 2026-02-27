# 📈 PROJETO 10: Customer Journey & NPS 3.0 (Earned Growth)

> **Status:** Engenharia de Crescimento (Baseado em NPS 3.0 e Earned Growth Rate)
> **Objetivo:** Automatizar a colheita de feedback e transformar clientes satisfeitos em motores de indicação (Referral), monitorando a saúde financeira da lealdade.

---

## 🚀 1. O Conceito "NPS 3.0"
Diferente do NPS comum, o **NPS 3.0** foca no **EGR (Earned Growth Rate)**. O sistema monitora dois pilares:
1.  **Retenção de Receita Líquida (NRR):** Clientes que voltam e gastam mais.
2.  **Novos Clientes Conquistados (ENC):** Clientes que vieram por indicação direta rastreada pelo bot.

---

## 🛠️ 2. Workflow de Interação (Zero Fricção)
Utilizamos **List Messages** da Meta Cloud API para que a avaliação seja feita com 2 toques.

### Gatilhos de Disparo (Triggers):
- `POST_PROCEDURE_2H`: Disparo 2 horas após o checkout para capturar o "Pico de Satisfação".
- `POST_PROCEDURE_24H`: Para procedimentos estéticos/dentários, o bot pergunta sobre o bem-estar e dor.
- `MILESTONE_6M`: Recall automático para limpeza/manutenção.

---

## 🔄 3. O Loop de Feedback Automatizado

### Para PROMOTORES (Nota 9-10):
- **Ação 1**: Bot envia link do Google Meu Negócio: *"Ficamos felizes! Poderia nos ajudar com uma avaliação de 5 estrelas?"*.
- **Ação 2**: Bot gera **Referral Link**: *"Indique um amigo pelo botão abaixo e ganhe R$ 50 de crédito em sua próxima visita"*.

### Para NEUTROS (Nota 7-8):
- **Ação**: Pergunta aberta para melhoria: *"O que faltou para sermos nota 10 hoje?"*.

### Para DETRATORES (Nota 0-6):
- **Ação 1**: Alerta **CÓDIGO LARANJA** no grupo de gestão.
- **Ação 2**: Mensagem de contenção imediata: *"Sentimos muito. O nosso gerente [Nome] entrará em contato em até 15 minutos para resolver isso pessoalmente."*.

---

## 💻 4. Estrutura Técnica (Payload Exemplo)

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "{{phone_number}}",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": { "type": "text", "text": "Sua Opinião Vale Ouro" },
    "body": { "text": "Como você avalia seu atendimento hoje na MoveMind? (0 é péssimo, 10 é excelente)" },
    "footer": { "text": "Escolha uma nota de 0 a 10" },
    "action": {
      "button": "Avaliar Agora",
      "sections": [
        {
          "title": "Promotores",
          "rows": [
            { "id": "nps_10", "title": "10 - Perfeito" },
            { "id": "nps_9", "title": "9 - Muito Bom" }
          ]
        },
        {
          "title": "Outros",
          "rows": [
            { "id": "nps_0_6", "title": "0 a 6 - Precisa Melhorar" }
          ]
        }
      ]
    }
  }
}
```

---

## 📈 5. Dashboards de LTV e Referral
- Integração com o **PROJETO 8 (BI)** para mostrar o gráfico de faturamento vindo de indicações vs. faturamento vindo de tráfego pago (Ads).

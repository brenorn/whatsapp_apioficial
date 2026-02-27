# 🚀 PROJETO 13: Google Ads Campaign Engineer (V2.0)

> **Status:** Engenharia de Investimento (Baseado em Performance Max e Conversão Offline / OCI)
> **Objetivo:** Automatizar a criação de campanhas de alta performance e treinar o algoritmo do Google com dados de vendas REAIS, garantindo que o orçamento seja gasto apenas com leads de alto valor.

---

## 🏗️ 1. O Conceito "Lucro Real no Algoritmo"
Anúncios comuns focam em "cliques". O **Ads Campaign Engineer** foca em **VENDAS PAGAS**.
- **Loop de Feedback:** O sistema vincula o clique inicial (GCLID) ao pagamento final.
- **OCI (Offline Conversion Import):** Envia o valor exato da venda de volta para o Google Ads, permitindo estratégias de lances baseadas em **ROAS Alvo**.

---

## 🛠️ 2. Workflow de Engenharia
1.  **Geração de Ativos:** O bot usa IA para criar 15 Headlines e 4 Descrições baseadas nos serviços mais lucrativos da semana (Projeto 8).
2.  **Criação Automática:** Uso da **Google Ads API v16** para criar `AssetGroups` em campanhas de Performance Max existentes.
3.  **Rastreamento (CAPI):** O bot captura o `gclid` no momento em que o lead chama no WhatsApp.
4.  **Sincronização de Conversão:** Quando o status no sistema da clínica vira "PAGO", o serviço envia um `POST` para o `ConversionUploadService`.

---

## 📊 3. Otimização de Budget (Guardião)
O bot monitora o painel de Ads diariamente e alerta no WhatsApp:
- *"Chefe, a campanha da 'Lente de Resina' teve um ROAS de 8.0 ontem. Recomendo aumentar o budget em 15%."*
- *"Atenção: A campanha de 'Limpeza' está com CPC muito alto. Pausei a veiculação para salvar seu orçamento."*

---

## 💻 4. Lógica Técnica (Exemplo de CAPI Offline)

```python
# Snippet conceitual de conversão offline
def upload_offline_conversion(customer_id, gclid, conversion_action_id, value):
    client = GoogleAdsClient.load_from_storage()
    click_conversion = client.get_type("ClickConversion")
    click_conversion.gclid = gclid
    click_conversion.conversion_action = conversion_action_id
    click_conversion.conversion_value = float(value)
    click_conversion.conversion_date_time = "2026-02-25 15:30:00+00:00"
    
    # Envio para o Google
    conversion_upload_service = client.get_service("ConversionUploadService")
    response = conversion_upload_service.upload_click_conversions(
        customer_id=customer_id, conversions=[click_conversion]
    )
```

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 11 (Monitoramento)**. Se a recepção reportar no grupo que as pessoas estão perguntando muito sobre um tratamento específico que não tem anúncio, o bot avisa: *"Gestor, detectei demanda reprimida por [X]. Quer que eu crie uma campanha agora?"*.

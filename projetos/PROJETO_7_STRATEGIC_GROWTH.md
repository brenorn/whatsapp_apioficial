# 🧲 PROJETO 7: Strategic Growth Engine (V2.0)

> **Status:** Inteligência de Mercado Proativa (Baseado em **Trend Analysis** e Social Listening)
> **Objetivo:** Antecipar tendências e garantir que a clínica esteja sempre à frente do mercado, conectando o que as pessoas estão buscando agora com a expertise do médico.

---

## 🏗️ 1. O Conceito "Market Oracle"
O crescimento estratégico não pode ser reativo. O **Growth Engine** atua como um pesquisador obcecado:
- **Trend Research:** Monitora Google Trends, pesquisas na Amazon e termos em alta no YouTube para o nicho de estética/saúde.
- **Social Listening:** Analisa as "Dores Invisíveis" comentadas em vídeos de concorrentes para municiar o **PROJETO 6**.

---

## 🛠️ 2. Workflow de Pesquisa Externa
1.  **Sondagem (PyTrends):** O bot executa um job semanal buscando termos em "Rising" (+100% de crescimento) no Brasil.
2.  **Análise de Sentimento:** IA estuda o "porquê" daquilo estar em alta.
3.  **Sugestão de Campanha:** O bot envia no WhatsApp do Gestor:
    - *"Detectei que a busca por 'Tratamento X pós-verão' subiu 300%. Sugiro uma campanha de Recaptura (Projeto 5) focada nisso."*
4.  **Integração de Pesquisa Profunda:** O robô utiliza ferramentas de pesquisa em bibliotecas, YouTube e fóruns para extrair dores reais (Ex: *"Medo de ficar com rosto boneco de cera"*).

---

## 💻 3. Exemplo de Lógica: O Agente de Trends
Arquivo sugerido: `server/marketing/strategy/trend_agent.py`

```python
from pytrends.request import TrendReq

def get_market_trends(keyword="estética facial"):
    pytrends = TrendReq(hl='pt-BR', tz=180)
    pytrends.build_payload([keyword], timeframe='today 1-m', geo='BR')
    rising = pytrends.related_queries()[keyword]['rising']
    
    # Envia para o Gemini interpretar e sugerir posts
    return gemini.analyze_trends(rising.to_dict())
```

---

## 📊 4. Estratégia "Alfinete no Mapa"
Este projeto garante que a clínica não mude de foco a cada tendência, mas sim que utilize a tendência para reforçar o seu **Alfinete no Mapa** (seu diferencial único).
- **Filtro de Coerência:** A IA descarta tendências que ferem a autoridade ou a "Alma" da marca definida no Projeto 6.

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 13 (Google Ads)**. Se uma tendência de busca é detectada, o bot sugere: *"Deseja que eu crie um conjunto de anúncios de Performance Max focado nesta nova tendência agora?"*.

---

## 📚 6. Documentação & Conexão
- **APIs:** PyTrends (Google Trends Wrapper), Gemini 2.5 Pro, Serper.dev (Search API).
- **Conexão Proj 7 -> Outros:** 
    - `-> Proj 6`: Entrega os "Temas Aleatórios" e "Dores" para a roteirização.
    - `-> Proj 24`: Apresenta os insights de mercado em um dashboard dentro do WhatsApp.

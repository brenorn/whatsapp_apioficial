# 📡 PROJETO 11: Group Intel & Daily Digest (V2.0)

> **Status:** Inteligência Operacional (Baseado em Communities API e NLP de Tendência)
> **Objetivo:** Monitorar a "pulsação" da empresa através dos grupos de WhatsApp, gerando resumos executivos e alertas de crise sem a necessidade de o CEO ler centenas de mensagens.

---

## 🏗️ 1. Arquitetura de Monitoramento
Para evitar as limitações de grupos pequenos da Cloud API, este projeto utiliza o conceito de **WhatsApp Communities (Comunidades)** e **Announcements Groups**.
- **Ingestão:** Webhooks capturam as mensagens onde o Bot é administrador.
- **Filtro de Ruído:** Algoritmo ignora figurinhas, áudios curtos (menos de 3s) e cumprimentos genéricos.
- **Context Window:** Agrupamento de mensagens por "Tópico" antes do envio para a IA.

---

## 📊 2. O Daily Digest (Resumo Executivo)
Enviado diariamente às 07:30 para o Admin.
### Estrutura do Digest:
1.  **🚨 Alertas Críticos:** Reclamações de pacientes, problemas com equipamentos ou falta de insumos detectados.
2.  **✅ Eficiência Operacional:** Quantas tarefas foram confirmadas como "feitas" nos grupos de operação.
3.  **😊 Clima Organizacional:** Análise de sentimento da equipe (Estão estressados? Felizes? Conflituosos?). *Link direto com o Projeto 9 (NR-01).*

---

## ⚡ 3. Alertas de Gatilho (Real-time)
O sistema possui um sensor de "Palavras de Risco". Se detectadas, o bot ignora o digest e envia um **Direct Message** imediato para o CEO.
**Exemplos de Gatilhos:** *"Justiça"*, *"Advogado"*, *"Pedir demissão"*, *"Erro médico"*, *"Procon"*.

---

## 💻 4. Lógica de Prompt (Inteligência de Resumo)

```yaml
context: "Você é um Analista de Operações focado em clínicas de alto padrão."
task: "Analise as mensagens do grupo [X] das últimas 24h."
output_format:
  - Resumo de 3 tópicos.
  - Tabela de Pendências detectadas.
  - Score de Tensão (0-100).
  - Sugestão de ação para o CEO.
```

---

## 🚀 5. Diferencial Competitivo
Integração com o **PROJETO 17 (Reuniões)**. Se um problema for recorrente nos grupos por 3 dias seguidos, o bot sugere automaticamente: *"Chefe, notei problemas repetidos com a Recepção. Deseja agendar uma reunião de 15 min hoje? Posso enviar o convite agora."*

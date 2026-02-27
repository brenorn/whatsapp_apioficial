# 📣 PROJETO 25: AI Conversational Outreach (V1.0)

> **Status:** Vendas Proativas Humanizadas (Baseado em Re-engagement Inteligente)
> **Objetivo:** Iniciar conversas de vendas de alto nível com a base atual de pacientes, utilizando a IA para personalizar a abordagem de acordo com o histórico e as dores específicas de cada cliente.

---

## 🏗️ 1. O Conceito "The Smart Reach-Out"
Diferente de um "Broadcast" frio, o **Conversational Outreach** inicia um diálogo:
- **Abordagem Relevante:** O bot olha o histórico (Projeto 22) e diz: *"Oi Maria, lembrei que você fez o tratamento X há 6 meses. Como está se sentindo? Notei que agora é uma ótima época para o retoque Y devido ao sol..."*.
- **Quebra de Objeções Real-time:** Utiliza o motor do **PROJETO 19 (Sales Negotiator)** para converter o "Agora não posso" em um agendamento.

---

## 🛠️ 2. Workflow de Ativação de Base
1.  **Segmentação (IA):** O sistema identifica um grupo de pacientes (Ex: *"Pacientes de Botox que não voltam há 5 meses"*).
2.  **Roteirização Pessoal:** O **PROJETO 6** gera uma "Frase de Abertura com Alma" para aquele grupo.
3.  **Disparo Cadenciado:** O sistema envia a mensagem e **aguarda a resposta**.
4.  **Condução de Conversa (AI Negotiator):** 
    - Se a paciente responde "Tenho interesse, mas tá caro", a IA entra com a matriz de decisão baseada em LTV (Projeto 19) para oferecer um bônus de fidelidade (Projeto 20).

---

## 💻 3. Exemplo de Lógica: O Nutridor de Leads
Arquivo sugerido: `server/marketing/outreach/proactive_sales.py`

```python
def start_proactive_conversation(patient_id):
    history = health_vault.get_history(patient_id)
    soul_copy = soul_copywriter.generate_opener(history)
    
    # Envia a mensagem via WhatsApp Cloud API
    whatsapp.send_text(patient_id.phone, soul_copy)
    
    # Coloca o status do chat em "Active Outreach"
    database.update_status(patient_id, "OUTREACH")
```

---

## 🚀 4. Diferencial IA
O bot não é invasivo. Ele usa **Gatilhos de Oportunidade**. Se o **PROJETO 7 (Trends)** detecta que um assunto está bombando, ele pode sugerir um Outreach focado: *"Oi João, vi que muita gente está com dúvida sobre [Assunto em Alta]. Como você já fez o procedimento conosco, queria te contar uma novidade..."*.

---

## 📚 5. Documentação & Conexão
- **Metodologia:** Tactical Empathy (FBI/Chris Voss) + Storytelling Emocional.
- **Conexão Proj 25 -> Outros:** 
    - `-> Proj 22`: Extrai os dados do prontuário para a personalização.
    - `-> Proj 19`: Gerencia o fechamento da venda.
    - `-> Proj 10`: Alimenta o Referral (Indicação) se a conversa for positiva.

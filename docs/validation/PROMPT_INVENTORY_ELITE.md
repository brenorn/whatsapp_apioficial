# 🔍 INVENTÁRIO TÉCNICO DE PROMPTS (MÓDULOS 9-25)
> **Gerado em:** 25/02/2026 01:57:15

## 🛠️ P9: NR1 Compliance
- **Arquivo:** `compliance/nr1_service.py`

### Prompt 1:
```text
Analise a seguinte resposta de um colaborador em uma auditoria NR-01:
        "{response_data.get('text')}"
        
        Identifique:
        1. Nível de Estresse (0-10)
        2. Presença de sinais de Burnout (Sim/Não)
        3. Necessidade de intervenção humana (Sim/Não)
        
        Retorne apenas em JSON.
```

---
## 🛠️ P10: NPS 3.0
- **Arquivo:** `marketing/nps_service.py`

> *Nenhum prompt 'f"""' detectado neste arquivo. Verifique a lógica interna.*

---
## 🛠️ P13: Google Ads
- **Arquivo:** `marketing/ads_service.py`

### Prompt 1:
```text
Dados de Tráfego de Ontem: {perf}
        Aja como um gestor de tráfego sênior. 
        O desempenho está bom? O que você recomendaria fazer com o orçamento?
        Responda em 3 bullet points curtos para WhatsApp.
```

---
## 🛠️ P14: SEO Machine
- **Arquivo:** `marketing/seo_service.py`

### Prompt 1:
```text
Aja como um Redator Médico Especialista em SEO (E-E-A-T).
        Transforme este conteúdo bruto em um artigo para blog:
        "{raw_content}"
        
        Requisitos:
        1. Título H1 magnético.
        2. Subtítulos H2 e H3 com palavras-chave de cauda longa.
        3. Linguagem técnica mas acessível (Autoridade Médica).
        4. Sugestão de Meta Description.
        5. Gere o código JSON-LD de Schema.org (MedicalWebPage).
```

---
## 🛠️ P16: Digital Twin
- **Arquivo:** `ai/digital_twin_service.py`

> *Nenhum prompt 'f"""' detectado neste arquivo. Verifique a lógica interna.*

---
## 🛠️ P17: Meeting Intel
- **Arquivo:** `ai/meeting_intel_service.py`

### Prompt 1:
```text
Analise a seguinte transcrição de consulta/reunião:
        "{transcript}"
        
        Extraia:
        1. Resumo Executivo (Bullet points).
        2. Action Items (Quem faz o que e quando).
        3. Código Mermaid.js para um Mapa Mental da discussão.
        
        Retorne em JSON estruturado.
```

---
## 🛠️ P19: Negotiation
- **Arquivo:** `commerce/negotiation_service.py`

### Prompt 1:
```text
{selected_persona}
        Objeção: "{objection}"
        Valor do Produto: {product_value}
        Margem Máxima Permitida: {max_discount * 100}%
```

---
## 🛠️ P22: Health Vault
- **Arquivo:** `ai/medical_engine.py`

### Prompt 1:
```text
Aja como um Assistente de Clínica Médica de Elite. 
        Resuma o histórico clínico para o doutor:
        "{history}"
        
        Foques: Alergias, Últimos procedimentos, Medicamentos em uso.
        Seja extremamente conciso e destaque Riscos em Negrito.
```

### Prompt 2:
```text
PACIENTE: {patient_data}
        PRESCRIÇÃO ATUAL: {prescribed_med}
        
        Existe alguma contraindicação ou risco alérgico? 
        Responda apenas "⚠️ ALERTA: [MOTIVO]" ou "✅ SEGURO".
```

---
## 🛠️ P25: AI Outreach
- **Arquivo:** `marketing/outreach_service.py`

### Prompt 1:
```text
Paciente: {patient['name']}
        Último Procedimento: {patient['last_procedure']} há {patient['days_ago']} dias.
        Aja como o Dr. Breno. Mande um 'Oi' sincero, pergunte como ela está e mencione que o efeito do {patient['last_procedure']} deve estar acabando. 
        Não seja vendedor chato. Seja um médico atencioso.
```

---

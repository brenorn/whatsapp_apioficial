# 🛡️ PROJETO 9: Escudo Psicossocial & Compliance NR-01 (V2.0)

> **Status:** Engenharia Detalhada (Inspirada na Portaria MTE nº 1.419/2024 e CNV Marshall Rosenberg)
> **Objetivo:** Blindar a empresa contra passivos trabalhistas e riscos psicossociais, garantindo uma comunicação de liderança assertiva, empática e legalmente segura.

---

## 🏛️ 1. Contexto Legal e Riscos (NR-01)
A partir de **maio de 2026**, as empresas brasileiras são obrigadas a gerenciar o **Risco Psicossocial** no seu Inventário de Riscos (PGR). Mensagens agressivas, demandas fora de hora e pressão desmedida via WhatsApp podem ser configuradas como:
- **Assédio Moral Organizacional**
- **Dano Moral Individual**
- **Sobrecarga Mental Ocupacional**

Este projeto atua como o **Buffer de Compliance** entre o ímpeto do gestor e o bem-estar da equipe.

---

## 🧠 2. Motor de Inteligência: LinguisticBuffer (CNV)
Utilizamos o framework de **Comunicação Não-Violenta (CNV)** para processar mensagens. O sistema decompõe o input bruto em quatro pilares (OFNR):
1.  **Observação:** Fatos reais sem julgamento.
2.  **Necessidade:** O que a clínica precisa para funcionar.
3.  **Sentimento:** Como a falha impacta o gestor.
4.  **Pedido:** Uma solicitação clara e acionável (em vez de uma ordem vaga).

---

## 🚦 3. Fluxo Técnico de Aprovação (Workflow)

1.  **Intercept:** O gestor envia uma mensagem (texto ou áudio) para o Bot da Clínica.
2.  **Análise de Risco:** O sistema detecta se a mensagem é para um **GRUPO** e avalia o "Índice de Agressividade".
3.  **Refino:** A IA gera uma versão polida mantendo a autoridade, mas removendo gatilhos de assédio.
4.  **Botão de Aprovação (WhatsApp Cloud API):** O bot envia uma mensagem interativa ao gestor:
    *   `[✅ Enviar Versão Polida]`
    *   `[✍️ Editar Manualmente]`
    *   `[⚠️ Ignorar Alerta (Risco Alto)]`

---

## 💻 4. Protótipo do Prompt de Refino (System Prompt)

```yaml
role: "Especialista em Psicologia Organizacional e Compliance NR-01"
method: "Marshall Rosenberg (NVC)"
rules:
  - Identifique "Vícios de Linguagem Tóxicos" (Ironia, Caps Lock, Ameaças).
  - Transforme ordens em pedidos claros baseados em fatos (Observação).
  - Garanta que a mensagem atenda aos requisitos de saúde mental do PGR.
```

---

## 📉 5. Benefícios Estratégicos (CEO Insight)
- **Jurídico:** Gera um "Log de Moderação", provando que a empresa toma medidas ativas para evitar assédio moral (Mitigação de Multas).
- **Cultura:** Reduz o *turnover* e o estresse da equipe, aumentando a produtividade.
- **Educação de Liderança:** O sistema ensina o gestor a se comunicar melhor com o tempo.

---

## 🛠️ 6. Próximos Passos
- [ ] Implementar `LinguisticBuffer` em `server/compliance/`.
- [ ] Criar template de botões interativos na Meta Graph API.
- [ ] Configurar interceptor de mensagens enviadas por administradores em grupos.

# 👁️ PROJETO 21: Digital Auditor (V2.0)

> **Status:** Visão Computacional de Compliance (Baseado em Gemini 1.5 Flash Vision)
> **Objetivo:** Garantir a padronização visual e de higiene da clínica através da auditoria automática de fotos enviadas via WhatsApp por funcionários. O "Olho do Dono" presente em todas as salas, 24/7.

---

## 🏗️ 1. O Conceito "Visual Standard"
Em clínicas de alto padrão, o detalhe é tudo. O **Digital Auditor** elimina a subjetividade da inspeção:
- **Zero Preguiça:** O bot não aceita "tá limpo", ele exige a imagem e a valida contra o padrão ouro.
- **Feedback Educativo:** Se algo está errado, o bot aponta na imagem onde está o problema (Ex: *"Cadeira desalinhada"*).

---

## 🛠️ 2. Workflow de Auditoria (Check-in/Out)
1.  **Gatilho Operacional:** O funcionário termina de limpar uma sala ou preparar uma recepção.
2.  **Envio de Mídia:** Envia uma foto do ambiente no grupo de 'Auditoria' (Projeto 11).
3.  **Análise Vision (Gemini 1.5 Flash):**
    - O bot compara a foto com o **Gold Standard** (Foto de referência do ambiente perfeito).
    - IA verifica itens específicos: Lixo, posição de quadros, limpeza do espelho, organização de bancada.
4.  **Veredito Instantâneo:**
    - `Score >= 90`: "Audit OK! Ótimo trabalho, [Nome]."
    - `Score < 90`: "Ainda não. Encontrei poeira na bancada e o espelho tem marcas. Por favor, corrija e mande outra foto."

---

## 💻 3. Prompt de Visão (Audit Protocol)

```yaml
role: "Inspetor de Qualidade 5S e Vigilância Sanitária"
task: "Compare a imagem REAL com a referência GOLD_STANDARD."
criteria:
  - Limpeza: Ausência de manchas, poeira e lixo.
  - Ordem: Alinhamento de móveis e objetos decorativos.
  - Compliance: Uso correto de EPIs se houver pessoas na foto.
output: "Score 0-100 e lista de 3 pontos de melhoria se houver."
```

---

## 📈 4. Dashboard de Excelência
Relatório mensal integrado ao **PROJETO 8 (CEO BI)**:
- **Setor mais limpo:** Ranking de salas.
- **Índice de Melhoria:** Quanto tempo a equipe demora para corrigir uma não-conformidade.
- **Padrão Estético:** Histórico visual da evolução da clínica.

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 18 (POP)**. Se o funcionário falhar 3 vezes na auditoria do mesmo item, o bot envia automaticamente o **Manual de Treinamento (PDF)** daquela tarefa no privado dele: *"Oi [Nome], notei dificuldade na limpeza do espelho. Veja aqui o passo-a-passo correto para facilitar seu trabalho!"*.

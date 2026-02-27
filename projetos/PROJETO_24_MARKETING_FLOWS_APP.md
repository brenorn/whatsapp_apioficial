# 📱 PROJETO 24: Marketing Command Flow (V1.0)

> **Status:** O "App dentro do WhatsApp" (Baseado em **WhatsApp Flows**)
> **Objetivo:** Eliminar a necessidade de dashboards externos. O dono da clínica gerencia toda a agência de marketing (Projetos 6, 7 e 12) através de interfaces interativas nativas dentro do WhatsApp.

---

## 🏗️ 1. O Conceito "No-Link Dashboard"
Gestores não querem abrir links e fazer login. O **Marketing Command** traz a gestão para a conversa:
- **Flows de Aprovação:** O robô envia um formulário nativo com o post gerado (Legenda + Imagem). O dono clica em "Aprovar" ou "Ajustar" ali mesmo.
- **Configuração de Campanha:** O dono define o "Alfinete no Mapa" e o "Arquétipo" através de seletores nativos (Dropdowns).

---

## 🛠️ 2. Módulos do "App In-Chat"
1.  **Mesa de Criação:** Botão que abre um Flow para criar um novo post:
    - Campo 1: Sugestão de Tema.
    - Campo 2: Objetivo (Venda/Autoridade/Engajamento).
2.  **Radar de Tendências:** Lista as 5 tendências do dia (Projeto 7). O dono clica em uma delas para disparar a criação automática da legenda (Projeto 6).
3.  **Analytics Compacto:** Relatório visual (Flow de leitura) com:
    - Alcance da semana.
    - Custo por Lead (Projeto 13).
    - Status dos OKRs (Projeto 23).

---

## 💻 3. Estrutura Técnica (JSON Flow)
Arquivo sugerido: `server/experience/marketing_flow.json`

```json
{
  "screens": [
    {
      "id": "CAMPAIGN_SETUP",
      "terminal": true,
      "data": {
        "archetypes": ["Mago", "Herói", "Sábio", "Explorador"],
        "goals": ["Captação de Leads", "Branding", "Venda Direta"]
      },
      "layout": {
        "children": [
          {"type": "Dropdown", "label": "Escolha o Arquétipo", "data_source": "archetypes"},
          {"type": "TextInput", "label": "Qual a Dor do Paciente hoje?"},
          {"type": "Footer", "label": "Gerar Postagem", "on_click_action": "submit"}
        ]
      }
    }
  ]
}
```

---

## 🚀 4. Diferencial IA
O bot atua como um **Agente Autônomo de Implementação**. Quando o dono aprova uma campanha no Flow, o sistema:
1. Envia a imagem para o Instagram.
2. Agenda o Broadcast de recuperação (Projeto 5).
3. Cria a regra de negociação específica no **Sales Negotiator** (Projeto 19).

---

## 📚 5. Documentação & Conexão
- **Tecnologia:** WhatsApp Business Flows (Graph API v21.0).
- **Segurança:** Payloads assinados via AES-256 GCM.
- **Conexão Proj 24 -> Outros:** 
    - `-> Proj 6 & 7`: É o controle remoto da inteligência criativa.
    - `-> Proj 12`: É o gatilho de publicação multicanal.

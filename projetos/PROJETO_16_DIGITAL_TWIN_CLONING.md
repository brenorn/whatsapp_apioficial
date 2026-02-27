# 👤 PROJETO 16: Digital Twin & Voice Cloning (V2.0)

> **Status:** Singularidade Mediada (Baseado em ElevenLabs Professional Voice e HeyGen Avatars)
> **Objetivo:** Multiplicar a presença do gestor/médico através de clones digitais de voz e vídeo, permitindo comunicação hiper-personalizada em escala humana no WhatsApp.

---

## 🏗️ 1. O Conceito "Presença Infinita"
O maior gargalo de uma empresa é o tempo do dono. O **Digital Twin** resolve isso:
- **Voz:** Sua voz envia áudios de orçamentos, boas-vindas e acompanhamento pós-operatório.
- **Vídeo:** Seu avatar digital explica procedimentos e responde dúvidas frequentes de forma visual e empática.

---

## 🛠️ 2. Workflow de Geração
1.  **Treinamento (Uma única vez):** O gestor envia áudios e um vídeo de 2 min para "ensinar" a IA.
2.  **Solicitação:** O bot detecta uma oportunidade (Ex: Novo agendamento de alto valor).
3.  **Criação de Conteúdo:**
    - IA gera o roteiro personalizado: *"Olá Maria, vi seu agendamento..."*.
    - **ElevenLabs API:** Gera o arquivo de áudio com a voz clonada.
    - **HeyGen API:** Gera o vídeo do avatar falando o roteiro com a voz clonada.
4.  **Entrega:** O bot envia o vídeo ou áudio no WhatsApp do cliente.

---

## 💻 3. Layer de Segurança (Identity Vault)
O acesso à clonagem é protegido por múltiplas camadas:
- **Admin Lock:** Somente o `ADMIN_PHONE` (Projeto 8) pode autorizar a geração de áudios com a voz do dono.
- **Context Guard:** A IA é instruída a nunca gerar conteúdos fora do contexto da clínica ou mensagens ofensivas.

---

## 📹 4. Aplicações de Elite
- **Boas-vindas VIP:** Receber um vídeo personalizado do médico assim que fecha o contrato.
- **Follow-up de Vendas:** O dono da clínica "ligando" (via áudio clonado) para um lead que não fechou o orçamento. *"Oi João, aqui é o Breno, notei que ficou uma dúvida no seu plano..."*.
- **Educação Continuada:** Tradução automática de vídeos técnicos para outros idiomas mantendo a sua voz original.

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 10 (NPS)**. Se um cliente der nota 2 (Detrator), o bot gera um áudio do dono em 30 segundos: *"Olá [Nome], soube do ocorrido e gostaria de pedir desculpas pessoalmente..."*. Isso reconquista clientes de forma impossível para humanos.

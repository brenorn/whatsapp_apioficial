# 🌐 PROJETO 12: Omnichannel Social Hub (V2.0)

> **Status:** Distribuição Multicanal Automatizada (Integrado com Graph API, TikTok & LinkedIn)
> **Objetivo:** Garantir a onipresença da clínica. O conteúdo gerado no **Projeto 6** é distribuído automaticamente para todas as redes sociais, respeitando os formatos nativos (Reels, Carrosséis, Documentos).

---

## 🏗️ 1. O Conceito "Post Once, Be Everywhere"
A IA não apenas "posta"; ela adapta a alma do conteúdo para cada plataforma:
- **Instagram:** Foco em **Reels** dinâmicos e **Carrosséis** estéticos. (Sim, Reels via Python são suportados!)
- **TikTok:** Vídeos rápidos com legendas nativas e hashtags de tendência do **Projeto 7**.
- **LinkedIn:** Posts de autoridade usando **PDFs Multi-página** (o formato carrossel nativo que gera 3x mais engajamento).

---

## 🛠️ 2. Workflow de Publicação
1.  **Gatilho de Aprovação:** O dono aprova a campanha no **Projeto 24 (WhatsApp Flows)**.
2.  **Preparação de Assets:**
    - O sistema hospeda as imagens/vídeos em URLs públicas (Buffer seguro).
    - Para o LinkedIn, converte as imagens em um único PDF de alta qualidade.
3.  **Execução Multi-Thread:**
    - **Insta:** Cria o container de Carousel ou Reel via `POST /media`.
    - **TikTok:** Faz o upload via `Direct Post API`.
    - **LinkedIn:** Registra o asset do documento e publica via `ugcPosts`.
4.  **Relatório de Entrega:** O bot avisa: *"Campanha publicada em 4 redes! [Links de acesso]"*.

---

## 💻 3. Especificações Técnicas (Omni-Poster)
Arquivo sugerido: `server/marketing/social/omni_publisher.py`

| Plataforma | Formato Principal | API Utilizada | Desafio Técnico |
| :--- | :--- | :--- | :--- |
| **Instagram** | Reels / Carousel | Graph API v21.0 | Necessita URL pública + Job de publicação. |
| **TikTok** | Vídeo / Photo Post | TikTok Content API | User Authorization OAuth2 obrigatório. |
| **LinkedIn** | PDF Document | LinkedIn V2 API | Registro de Asset binário complexo. |
| **Facebook** | Image / Video | Page Graph API | Sincronia com conta de anúncios (CAPI). |

---

## 🚀 4. Diferencial IA
Integração com o **PROJETO 4 (CAPI Tracker)**. O sistema não apenas posta; ele gera uma URL própria para cada rede (`track_uid`). Se alguém vem do TikTok e compra pelo WhatsApp, o sistema avisa o CRM: *"Venda originada do post tático de Terça-feira no TikTok"*.

---

## 📚 5. Documentação & Conexão
- **Referência:** Consulte o `API_CONNECTIONS_GUIDE.md` para chaves e métodos de conexão.
- **Conexão Proj 12 -> Outros:** 
    - `<- Proj 6`: Recebe os assets criados.
    - `-> Proj 13`: Alimenta o remarketing para quem clicou nos links orgânicos.

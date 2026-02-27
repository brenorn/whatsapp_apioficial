# 🗝️ Guia Mestre de Conexões e APIs (V1.0)

> **Importante:** Este documento é o seu manual de referência técnica. Guarde-o para quando iniciarmos a implementação de cada módulo.

---

## 🏥 1. Google MedGemma (Inteligência Médica)
**Utilidade:** Análise de prontuários, imagens dermatológicas e apoio à decisão clínica.

*   **Como Obter:**
    1.  Acesse o [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/medgemma).
    2.  Clique em "Enable" (Habilitar) na API do Vertex AI.
    3.  Aceite os termos da **Health AI Developer Foundation**.
    4.  Crie uma Service Account no Google Cloud com a role `Vertex AI User`.
*   **SDK (Python):** `pip install google-cloud-aiplatform`
*   **Atenção:** Os modelos 4B são otimizados para imagens/mobile, e os 27B para raciocínio clínico complexo.

---

## 📸 2. Instagram Graph API (Reels & Carrosséis)
**Utilidade:** Postagem automática de conteúdo gerado pela IA.

### A) Reels (Sim, é possível!)
Ao contrário do que se pensava, os Reels são postáveis via API desde 2022.
*   **Endpoint:** `POST /{ig-user-id}/media`
*   **Parâmetro:** `media_type=REELS`
*   **Requisitos:** Vídeo MP4/MOV, 9:16, max 1GB, max 90 segundos.
*   **Processo:** 
    1. Envia o vídeo (URL pública).
    2. Recebe o Container ID.
    3. Publica o Container usando `media_publish`.

### B) Carrosséis (Carousel)
*   **Processo de 3 Etapas:**
    1. Criar containers individuais para cada imagem/vídeo (`is_carousel_item=true`).
    2. Criar um container pai do tipo `CAROUSEL` contendo a lista de IDs dos filhos.
    3. Publicar o ID do container pai.

---

## 🎥 3. TikTok Content Posting API
**Utilidade:** Postagem de vídeos curtos e fotos (carrosséis).

*   **Como Obter:** Cadastre-se em [TikTok for Developers](https://developers.tiktok.com/).
*   **Scopes:** `video.publish` e `video.upload`.
*   **Método:** `Direct Post`. Você pode enviar o arquivo bruto (`FILE_UPLOAD`) ou via URL (`PULL_FROM_URL`).

---

## 💼 4. LinkedIn API (Posts de Autoridade)
**Utilidade:** Conteúdo técnico para fortalecer o branding do médico.

*   **Carrosséis:** No LinkedIn, a melhor forma de fazer carrosséis é postando um **Documento PDF Multi-página**. Cada página vira um slide.
*   **Processo:** Register Asset (PDF) -> PUT Binary -> Create UGC Post (User Generated Content) com `shareMediaCategory: DOCUMENT`.

---

## 🎯 5. Google Ads API (Máquina de Tráfego)
**Utilidade:** Controle de anúncios direto pelo WhatsApp.

*   **Como Obter:**
    1. Logue na sua conta **MCC (Manager Account)**.
    2. Vá em `Ferramentas e Configurações` -> `Centro de API`.
    3. Obtenha o **Developer Token** (22 caracteres).
*   **Credenciais Gerais:** Você precisará de `Developer Token`, `Client Customer ID`, `Client ID`, `Client Secret` e `Refresh Token`.

---

## 📂 6. Resumo de Servições por Nível

| Nível de Serviço | Projetos Incluídos | Foco Principal |
| :--- | :--- | :--- |
| **Básico (Essencial)** | P1, P2, P3, P11 | Vendas e Atendimento (STT, Pix, Flows) |
| **Intermediário (Growth)** | + P6, P12, P13, P14 | Marketing e Ads (Social, SEO, Tráfego) |
| **Avançado (Elite)** | + P8, P15, P16, P22, P23 | IA Pura (MedGemma, Digital Twin, BI, OKR) |

---

## 📝 Exemplo de Código Base (Multi-Post Carousel)

```python
# Conceito para Instagram Carousel
def post_insta_carousel(images_urls, caption, access_token, ig_user_id):
    # 1. Cria itens individuais
    item_ids = []
    for url in images_urls:
        res = requests.post(f"https://graph.facebook.com/v21.0/{ig_user_id}/media", 
                            data={'image_url': url, 'is_carousel_item': 'true', 'access_token': access_token})
        item_ids.append(res.json()['id'])
    
    # 2. Cria o container álbum
    album_res = requests.post(f"https://graph.facebook.com/v21.0/{ig_user_id}/media",
                              data={'media_type': 'CAROUSEL', 'children': item_ids, 'caption': caption, 'access_token': access_token})
    
    # 3. Publica
    publish_res = requests.post(f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish",
                                data={'creation_id': album_res.json()['id'], 'access_token': access_token})
    return publish_res.json()
```

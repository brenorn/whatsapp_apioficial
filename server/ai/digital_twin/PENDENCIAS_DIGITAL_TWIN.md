# 🎙️ Digital Twin: Clonagem de Voz e Avatar (P16 e P23)

O módulo Digital Twin transforma textos analíticos em vozes 100% humanizadas usando a tecnologia de clonagem da ElevenLabs. O WhatsApp enviará o áudio como se o médico estivesse gravando na hora.

---

## 🔐 1. Variáveis de Ambiente (.env) Exigidas

Adicione as seguintes chaves ao seu `.env` raiz:

### ElevenLabs (Clonagem de Voz)
```env
ELEVENLABS_API_KEY="sk_sua_chave_aqui"

# O Voice ID gerado no VoiceLab (Ex: voz clonada do CEO/Médico)
ELEVENLABS_DEFAULT_VOICE_ID="seu_voice_id_aqui" 
```

---

## 🛠️ 2. Como Clonar a Voz do Médico (Passo a Passo)

Para que o robô não tenha "voz de locutor de aeroporto", o médico precisa gravar 1 minuto de sua voz natural e injetar na ElevenLabs:

1. Acesse [ElevenLabs (VoiceLab)](https://elevenlabs.io/app/voice-lab).
2. Clique em **"Add a new voice"** > **"Instant Voice Cloning"**.
3. Faça o upload de um áudio bem limpo do médico falando (um áudio de WhatsApp sem barulho de fundo já serve).
4. Dê um nome (ex: `Voz Oficial Dr. Breno`).
5. Copie o **Voice ID** (um código longo na aba ID).
6. Cole no seu `.env` na variável `ELEVENLABS_DEFAULT_VOICE_ID`.

---

## 🧠 3. O Fluxo de Trabalho (WhatsApp)

Quando uma intenção específica for acionada (ex: `WELCOME_PATIENT` ou `CLINICAL_BRIEFING`), o orquestrador fará o seguinte:
1. Pede ao **Gemini 2.5 Pro** que escreva um texto.
2. Injeta o texto no **ElevenLabs Engine**.
3. A ElevenLabs devolve um arquivo `.mp3` contendo respirações, entonações hiper-realistas e emoção.
4. O `WhatsAppCloudClient` pega esse arquivo na pasta `/server/assets/audio` e dispara como se fosse uma mensagem de áudio nativa no chat do paciente.

---

## 🎥 4. Próxima Fase: Gêmeo de Vídeo (HeyGen - P23)
*Em construção.* Futuramente, ligaremos a mesma API de áudio aos motores visuais da HeyGen para que a clínica envie vídeos do doutor cumprimentando o paciente pelo nome.

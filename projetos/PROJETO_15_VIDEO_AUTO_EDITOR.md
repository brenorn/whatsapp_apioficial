# 🎬 PROJETO 15: AI Video Auto-Editor (V2.0)

> **Status:** Pós-Produção Automatizada (Baseado em Whisper, MoviePy e FFmpeg)
> **Objetivo:** Transformar vídeos brutos gravados via celular em conteúdos magnéticos com ritmo acelerado, eliminando silêncios e adicionando legendas dinâmicas estilo Alex Hormozi.

---

## 🏗️ 1. O Conceito "Edição Invisível"
O bot não apenas "guarda" o vídeo, ele o **refina**. Através de visão computacional e análise de áudio, o editor executa tarefas que levariam horas em minutos:
- **Jump Cuts:** Remove cada micro-silêncio para manter a atenção no máximo.
- **Smart Captions:** Legendas que "pulam" na tela conforme a fala.
- **B-Roll Suggestion:** Sugere onde inserir imagens de apoio baseadas no assunto (Projeto 14).

---

## 🛠️ 2. Workflow de Edição
1.  **Envio:** O gestor manda o vídeo bruto para o WhatsApp.
2.  **Audio Analysis (Whisper):** O sistema gera a transcrição com marcação de tempo palavra por palavra.
3.  **Processamento FFmpeg:**
    - Identifica e remove trechos de silêncio (Silence Detection).
    - Aplica o arquivo `.ass` de legendas dinâmicas (Montserrat Black, Emojis, Destaque de cor).
4.  **Entrega:** O bot devolve dois arquivos:
    - `Master_Vertical.mp4`: Pronto para Reels/TikTok.
    - `Master_Horizontal.mp4`: Pronto para YouTube/Blog.

---

## 💻 3. Lógica de Jump Cut (Python Snippet)
O sistema usa o volume do áudio para decidir onde cortar:

```python
from pydub import AudioSegment, silence

def detect_cuts(audio_path):
    audio = AudioSegment.from_file(audio_path)
    # Detecta silêncios maiores que 300ms com volume abaixo de -35dB
    silent_ranges = silence.detect_silence(audio, min_silence_len=300, silence_thresh=-35)
    # Inverte para pegar os intervalos de FALA
    return get_speech_intervals(silent_ranges)
```

---

## 🎨 4. Estilo Visual "Magnetic"
- **Fonte:** Montserrat Black 900.
- **Cor de Destaque:** Amarelo (#FFFF00) ou Verde Neon (#39FF14) para palavras de impacto.
- **Zoom Dinâmico:** O bot aplica um leve zoom (10%) nos momentos de ênfase para dar dinamismo ao vídeo "cabeça falante".

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 12 (Omnichannel)**. Assim que o vídeo é editado, o bot pergunta: *"Video editado com sucesso! Deseja que eu agende a postagem no TikTok e LinkedIn agora?"*.

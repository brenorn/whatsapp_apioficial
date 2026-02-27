# 🎨 PROJETO 6: Social Media Command Center (V2.0)

> **Status:** Engenharia de Design Poético (Inspirado no Método "IA COM ALMA" e "Método Triângulo")
> **Objetivo:** Transformar o WhatsApp na agência de criação definitiva da clínica, gerando conteúdos que transcendem o clichê e tocam a "alma" do paciente através de conexões magnéticas e narrativa emocional.

---

## 🏛️ 1. Filosofia: O Motor de Design Poético
Não geramos apenas "imagens e textos"; criamos universos visuais e narrativos baseados em **Arquétipos Narrativos**:
- **O Mago:** Fotos com iluminação volumétrica e mistério (procedimentos que transformam).
- **O Herói:** Ângulos baixos e alto contraste (superação de dores e traumas estéticos).
- **O Sábio:** Simetria e luz suave (autoridade médica e conhecimento técnico).

---

## 🛠️ 2. Workflow "IA COM ALMA"
O sistema utiliza a triangulação de 3 elementos para cada post:
1.  **Alfinete no Mapa:** O foco único do médico (Ex: "Especialista em olhar natural").
2.  **Tema Aleatório:** Uma metáfora cotidiana (Ex: "Uma xícara de café que esfriou").
3.  **Dor Invisível:** A necessidade que ninguém fala (Ex: "O medo de não se reconhecer no espelho").

**O Bot conecta os três em um roteiro de 90 segundos que gera "Conexão Magnética".**

---

## 🖼️ 3. Carousel & Multi-Asset Creation
O bot automatiza a criação de carrosséis estratégicos:
- **Slide 1 (Gancho/Hook):** Frase magnética com tom de "clickbait" ético.
- **Slides 2-4 (Desenvolvimento):** Exploração da "Dor Invisível" e conexão com a solução.
- **Slide Final (CTA):** Chamada para ação direta via Link do WhatsApp (Projeto 3/19).

---

## 💻 4. Exemplo de Prompt (Soulful Copywriter)
Arquivo sugerido: `server/marketing/social/soul_copywriter.py`

```python
def generate_soulful_script(alfinete, tema, dor):
    prompt = f"""
    Aja como um Diretor de Criação com Alma. 
    Alfinete: {alfinete}
    Tema Aleatório: {tema}
    Dor Invisível: {dor}
    
    Tarefa: Crie um roteiro de 90s. 
    Misture a metáfora do tema com a profundidade da dor. 
    Evite clichês de marketing digital. Foque em humanidade.
    """
    return gemini.generate(prompt)
```

---

## 🚀 5. Diferencial IA
Integração com o **PROJETO 15 (Vídeo)** e **PROJETO 16 (Digital Twin)**. O bot sugere: *"Este roteiro de Carrossel ficou incrível. Deseja que eu transforme ele em um roteiro de Reels para o seu Avatar Digital falar com sua voz clonada agora?"*.

---

## 📚 6. Documentação & Conexão
- **Tecnologia:** Gemini 2.5 Pro + Midjourney/DALL-E 3 API.
- **Metodologia:** IA COM ALMA (Triangulação Narrativa).
- **Conexão Proj 6 -> Outros:** 
    - `-> Proj 12`: Distribui o conteúdo gerado para Instagram/Facebook.
    - `-> Proj 24`: Recebe a aprovação do gestor via WhatsApp Flows.

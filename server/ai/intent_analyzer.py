from typing import Dict, Any

class IntentAnalyzer:
    """
    Roteador de Intenções para Economia e Segurança de Tokens.
    Em vez de chamar a LLM (Gemini) só para dizer "Você quer cancelar?",
    ele usa Regex/Match antes para o fluxo 'Slow Path'.
    """

    @staticmethod
    def is_fast_path(text: str) -> bool:
        """Se for confirmação óbvia, não instancie o LLM"""
        text_upper = str(text).upper().strip()
        confirm_keywords = ['SIM', 'OK', 'BELEZA', 'PODE SER', 'FECHADO', 'CONFIRMADO']
        if text_upper in confirm_keywords:
            return True
        return False

    @staticmethod
    def identify_intent(text: str, context: dict = None) -> Dict[str, Any]:
        """
        No futuro, pode bater numa LLM barata (Flash) ou num modelo local NLP,
        mas o padrão BMAD pede RegEx/Heuristica primeiro.
        """
        text_upper = str(text).upper()
        
        # 1. Intenção de Urgência (Crise)
        if any(w in text_upper for w in ["SOCORRO", "HOSPITAL", "URGENCIA", "DOR", "MORRENDO"]):
             return {"intent": "CRITICAL", "is_crisis": True}
             
        # 2. Replanejamento / Cancelamento
        if any(w in text_upper for w in ["CANCELAR", "REMARCAR", "MUDAR HORARIO", "OUTRO DIA"]):
            return {"intent": "RESCHEDULE", "is_crisis": False}
            
        # 3. Agendamento Novo (Aciona o WhatsApp Flows Módulo 3)
        if any(w in text_upper for w in ["AGENDAR", "MARCAR", "HORARIO", "CONSULTA", "QUERIA IR"]):
            return {"intent": "SCHEDULE", "wants_booking": True, "is_crisis": False}
            
        # 4. Prova Social / Depoimento (Gatilho para Projeto 6)
        if any(w in text_upper for w in ["MUITO BOM", "AMEI", "OBRIGADO", "RESULTADO", "DEPOIMENTO", "RECOMENDO", "GRATIDÃO"]):
            return {"intent": "TESTIMONIAL", "is_social_proof": True, "is_crisis": False}
            
        # 5. Planejamento Estratégico (Projeto 7)
        if any(w in text_upper for w in ["PLANO", "SEMANAL", "CRONOGRAMA", "CALENDARIO", "O QUE POSTAR", "ESTRATEGIA"]):
            return {"intent": "STRATEGIC_PLAN", "is_crisis": False}
        
        # 6. Transformação de Conteúdo (Projeto 7) - Quando o texto é muito longo (Provável Artigo)
        if len(text) > 400 or any(w in text_upper for w in ["ARTIGO", "TEXTO LONGO", "TRANSFORME", "RESUMA"]):
             return {"intent": "CONTENT_TRANSFORM", "is_crisis": False}
             
        # 7. Relatórios Gerenciais / BI (Projeto 8)
        if any(w in text_upper for w in ["QUANTO FATURAMOS", "RELATORIO", "VENDAS DE HOJE", "METRICAS", "DESEMPENHO", "KPI"]):
            return {"intent": "ADMIN_REPORT", "is_crisis": False}

        # 8. Compliance NR-01 e Saúde Mental (Projeto 9)
        if any(w in text_upper for w in ["NR-01", "NR1", "SEGURANÇA", "AUDITORIA", "BURNOUT", "CIPA", "ESTRESSE", "PSICOSSOCIAL"]):
            return {"intent": "NR1_COMPLIANCE", "is_crisis": False}
        
        # 9. NPS e Satisfação (Projeto 10)
        # Se for apenas um número entre 0 e 10
        if text_upper.isdigit() and 0 <= int(text_upper) <= 10:
             return {"intent": "NPS_RESPONSE", "score": int(text_upper)}
        if any(w in text_upper for w in ["NOTA", "AVALIAÇÃO", "MINHA NOTA"]):
             return {"intent": "NPS_RESPONSE"}
        
        # 10. Google Ads (Projeto 13)
        if any(w in text_upper for w in ["ADS", "CAMPANHA", "ANUNCIO", "TRAFEGO", "GOOGLE ADS"]):
             return {"intent": "GOOGLE_ADS", "is_crisis": False}
        
        # 11. Mind Maps e Estruturação (Projeto 17)
        if any(w in text_upper for w in ["MAPA MENTAL", "MINDMAP", "FLUXOGRAMA", "DIAGRAMA", "RESUMO DE REUNIÃO", "ATA"]):
             return {"intent": "MINDMAP", "is_crisis": False}
        
        # 12. Padronização Operacional (Projeto 18)
        if any(w in text_upper for w in ["CRIAR POP", "PROCEDIMENTO", "PADRONIZAR", "5W2H", "NORMA"]):
             return {"intent": "POP_CREATE", "is_crisis": False}
        
        # 13. Negociação de Vendas (Projeto 19)
        if any(w in text_upper for w in ["CARO", "DESCONTO", "VALOR", "PREÇO", "BAIXAR", "MELHORAR", "CONSEGUE FAZER"]):
             return {"intent": "NEGOTIATION", "is_crisis": False}
        
        # 14. Fidelidade e Gamificação (Projeto 20)
        if any(w in text_upper for w in ["PONTOS", "NÍVEL", "STATUS", "PONTUAÇÃO", "FIDELIDADE", "RECOMPENSA"]):
             return {"intent": "LOYALTY_STATUS", "is_crisis": False}
        
        # 15. Inteligência Médica e Prontuário (Projeto 22)
        if any(w in text_upper for w in ["PRONTUÁRIO", "ALERGIA", "HISTÓRICO", "PACIENTE", "RESUMO DA MARIA", "ANAMNESE"]):
             return {"intent": "MEDICAL_INFO", "is_crisis": False}

        # 16. Gestão de Marketing / Mini-App (Projeto 24)
        if any(w in text_upper for w in ["APP", "MENU", "GERENCIAR", "CAMPANHAS", "PAINEL", "COMANDO"]):
             return {"intent": "MARKETING_APP", "is_crisis": False}
        
        # 17. Prospecção Ativa / Outreach (Projeto 25)
        if any(w in text_upper for w in ["PROSPECÇÃO", "BUSCAR PACIENTES", "REENGAJAR", "BUSCA ATIVA", "VENDA ATIVA"]):
             return {"intent": "OUTREACH_START", "is_crisis": False}

        # 18. Neutra (Dúvida comum, passa pra Langchain/Gemini responder)
        return {"intent": "GENERAL_QUESTION", "wants_booking": False, "is_social_proof": False, "is_crisis": False}

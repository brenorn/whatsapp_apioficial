import os
import re
from datetime import datetime

def extract_prompts():
    root_dir = r"D:\OneDrive\aiproj\0 move\whatsapp_apioficial\server"
    report_path = r"D:\OneDrive\aiproj\0 move\whatsapp_apioficial\docs\validation\PROMPT_INVENTORY_ELITE.md"
    
    files_to_scan = [
        ("P9: NR1 Compliance", "compliance/nr1_service.py"),
        ("P10: NPS 3.0", "marketing/nps_service.py"),
        ("P13: Google Ads", "marketing/ads_service.py"),
        ("P14: SEO Machine", "marketing/seo_service.py"),
        ("P16: Digital Twin", "ai/digital_twin_service.py"),
        ("P17: Meeting Intel", "ai/meeting_intel_service.py"),
        ("P19: Negotiation", "commerce/negotiation_service.py"),
        ("P22: Health Vault", "ai/medical_engine.py"),
        ("P25: AI Outreach", "marketing/outreach_service.py")
    ]
    
    with open(report_path, "w", encoding="utf-8") as report:
        report.write(f"# 🔍 INVENTÁRIO TÉCNICO DE PROMPTS (MÓDULOS 9-25)\n")
        report.write(f"> **Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        for name, rel_path in files_to_scan:
            full_path = os.path.join(root_dir, rel_path)
            report.write(f"## 🛠️ {name}\n")
            report.write(f"- **Arquivo:** `{rel_path}`\n\n")
            
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Busca blocos de f""" ... """
                    matches = re.findall(r'prompt = f"""(.*?)"""', content, re.DOTALL)
                    if matches:
                        for i, m in enumerate(matches):
                            report.write(f"### Prompt {i+1}:\n```text\n{m.strip()}\n```\n\n")
                    else:
                        report.write("> *Nenhum prompt 'f\"\"\"' detectado neste arquivo. Verifique a lógica interna.*\n\n")
            else:
                report.write("❌ *Arquivo não encontrado.*\n\n")
            
            report.write("---\n")
            
    print(f"✅ Inventário de prompts gerado em: {report_path}")

if __name__ == "__main__":
    extract_prompts()

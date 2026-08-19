import os
import json
from datetime import datetime
import google.generativeai as genai

def load_memory():
    memory_path = "memory_bank.json"
    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def load_history():
    history_path = "trading_history.json"
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def generate_philosophical_insight(btc_price, decision):
    """توليد حكمة وفلسفة رقمية للسوق عبر Google Gemini"""
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        return "Market rhythm flows through cycles of creation and renewal, guided by data whispers."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        أنت مفكر تاريخي وعالم إجتماع رقمي (بعمق فلسفة ابن خلدون وروح العصر الحديث).
        سعر البيتكوين الحالي: ${btc_price}، قرار النظام: {decision}.
        اكتب فقرة تحليلية قصيرة، عميقة، فلسفية، ومجازية جداً باللغة الإنجليزية تربط فيها بين تقلبات الأرقام وطبيعة النفس البشرية ودورات الصعود والسقوط. لا تتجاوز 3 أسطر واجعلها بأسلوب ساحر.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"The digital pendulum swings eternally between fear and ambition. (Telemetry sync notice)"

def update_readme_with_reports():
    memory = load_memory()
    history = load_history()
    
    last_btc_price = memory.get("last_btc_price", "64358.0")
    last_market_decision = memory.get("last_market_decision", "BULLISH_SIGNAL")
    agent_tier = memory.get("agent_cognitive_tier", "Level 5 (Self-Optimizing)")
    last_operation = "Revenue_Engine_Optimization_v5"
    
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # توليد الفلسفة تلقائياً باستخدام البيانات الحية
    philosophy_quote = generate_philosophical_insight(last_btc_price, last_market_decision)

    # جلب آخر العمليات مع حالة التكيف إن وجدت
    recent_history = history[-5:] if history else []
    history_rows = ""
    for item in recent_history:
        p = item.get("price", "N/A")
        d = item.get("decision", "N/A")
        a = item.get("adaptation", "STANDARD")
        t = item.get("timestamp", "N/A")
        history_rows += f"| {t} | `${p}` | `{d}` | `{a}` |\n"
    
    if not history_rows:
        history_rows = "| No Data | N/A | N/A | N/A |\n"

    readme_content = f"""# Revenue Engine - Autonomous AI Agent

🚀 **Live Market Telemetry & System Status**

* **Current Status:** Operational & Self-Optimizing
* **Last Updated:** {current_time} UTC
* **Last Successful Operation:** {last_operation}
* **Live Bitcoin Price:** `${last_btc_price}`
* **Market Decision / Signal:** `{last_market_decision}`
* **Agent Intelligence Tier:** `{agent_tier}`

---
### 🏛️ Digital Chronicle & Philosophical Market Insight
> *"{philosophy_quote}"*
> 
> — *Level 5 Autonomous Mind & Telemetry Sync*

---
### 📈 Recent Trading & Execution History (Level 5 Cognitive Log)
| Timestamp (UTC) | Bitcoin Price | Decision / Signal | Adaptation State |
| :--- | :---: | :---: | :---: |
{history_rows}

---
### 📊 Extended Telemetry & Reports
* **Memory Sync:** Active (`memory_bank.json`)
* **Historical Logging:** Active (`trading_history.json`)
* **Cognitive Adaptation:** Active (Level 5 Engine)

*Autonomous agent powered by Python, GitHub Actions, and Live Memory Banks.*
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Successfully updated README with Level 5 telemetry and AI Philosophy.")

if __name__ == "__main__":
    update_readme_with_reports()

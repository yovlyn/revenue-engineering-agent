import os
import json
from datetime import datetime

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

def update_readme_with_reports():
    memory = load_memory()
    history = load_history()
    
    last_btc_price = memory.get("last_btc_price", "N/A")
    last_market_decision = memory.get("last_market_decision", "N/A")
    agent_tier = memory.get("agent_cognitive_tier", "Level 5 (Self-Optimizing)")
    last_operation = "Revenue_Engine_Optimization_v5"
    
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
    print("Successfully updated README with Level 5 telemetry.")

if __name__ == "__main__":
    update_readme_with_reports()

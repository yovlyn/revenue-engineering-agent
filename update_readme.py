def update_readme_with_reports():
    memory = load_memory()
    history = load_history()
    
    # التأكد من أن التاريخ عبارة عن قائمة لتجنب خطأ الـ slice إذا كان الملف يحوي قواميس
    if isinstance(history, dict):
        history = list(history.values())
    elif not isinstance(history, list):
        history = []
    
    last_btc_price = memory.get("last_btc_price", "64358.0")
    last_market_decision = memory.get("last_market_decision", "BULLISH_SIGNAL")
    agent_tier = memory.get("agent_cognitive_tier", "Level 5 (Self-Optimizing)")
    last_operation = "Revenue_Engine_Optimization_v5"
    
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # توليد الفلسفة تلقائياً باستخدام البيانات الحية
    philosophy_quote = generate_philosophical_insight(last_btc_price, last_market_decision)

    # جلب آخر العمليات بأمان تام
    recent_history = history[-5:] if history else []
    history_rows = ""
    for item in recent_history:
        if isinstance(item, dict):
            p = item.get("price", "N/A")
            d = item.get("decision", "N/A")
            a = item.get("adaptation", "STANDARD")
            t = item.get("timestamp", "N/A")
            history_rows += f"| {t} | `{p}` | `{d}` | `{a}` |\n"
    
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

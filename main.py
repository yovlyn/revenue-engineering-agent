import json
import os
from datetime import datetime
from self_healing import self_heal_execution
from memory_engine import save_to_memory, load_memory
from api_engine import fetch_market_data

def append_to_history(data):
    """حفظ العملية في السجل التاريخي"""
    history_file = "trading_history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    # إضافة العملية الجديدة مع التوقيت
    data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    history.append(data)
    
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def core_operational_task():
    print("Agent accessing API for live market data...")
    btc_price = fetch_market_data("BTC")
    
    # منطق اتخاذ القرار (Level 4 Logic)
    decision = "HOLD"
    if isinstance(btc_price, float):
        if btc_price < 60000:
            decision = "BUY_SIGNAL"
        else:
            decision = "SELL_SIGNAL"
    
    # حفظ النتائج في الذاكرة طويلة المدى
    save_to_memory("last_market_decision", decision)
    save_to_memory("last_btc_price", btc_price)
    
    # حفظ العملية في السجل التاريخي
    append_to_history({"price": btc_price, "decision": decision})
    
    return f"Decision: {decision}, Price: {btc_price}"

if __name__ == "__main__":
    response = self_heal_execution(core_operational_task)
    print("Status:", response)

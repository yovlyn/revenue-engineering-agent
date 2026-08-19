import json
import os
from datetime import datetime
from self_healing import self_heal_execution
from memory_engine import save_to_memory, load_memory
from api_engine import fetch_market_data

def get_moving_average(history, periods=5):
    """حساب المتوسط المتحرك لآخر عدد من العمليات"""
    if len(history) < periods:
        return None
    recent_prices = [item['price'] for item in history[-periods:]]
    return sum(recent_prices) / len(recent_prices)

def append_to_history(data):
    history_file = "trading_history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try: history = json.load(f)
            except: history = []
    
    data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    history.append(data)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)
    return history

def core_operational_task():
    print("Agent analyzing market trends...")
    btc_price = fetch_market_data("BTC")
    
    # 1. جلب التاريخ لتحليل الاتجاه
    history_file = "trading_history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try: history = json.load(f)
            except: history = []
            
    ma = get_moving_average(history, periods=3) # متوسط آخر 3 عمليات
    
    # 2. منطق القرار الذكي (مقارنة السعر الحالي بالمتوسط)
    decision = "HOLD"
    if ma:
        if btc_price > ma:
            decision = "BULLISH_SIGNAL" # السعر أعلى من المتوسط (اتجاه صعودي)
        else:
            decision = "BEARISH_SIGNAL" # السعر أقل من المتوسط (اتجاه هبوطي)
    else:
        # قرار أولي إذا لم يتوفر سجل كافٍ
        decision = "INITIALIZING"
    
    # 3. الحفظ
    save_to_memory("last_market_decision", decision)
    save_to_memory("last_btc_price", btc_price)
    append_to_history({"price": btc_price, "decision": decision})
    
    return f"Decision: {decision}, Price: {btc_price}, MA: {ma}"

if __name__ == "__main__":
    response = self_heal_execution(core_operational_task)
    print("Status:", response)

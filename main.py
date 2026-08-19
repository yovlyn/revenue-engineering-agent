import json
import os
from datetime import datetime
from self_healing import self_heal_execution
from memory_engine import save_to_memory, load_memory
from api_engine import fetch_market_data

def evaluate_and_adapt_strategy(history):
    """المستوى الخامس: تقييم الأداء السابق وتعديل استراتيجية التفكير ذاتياً"""
    if len(history) < 3:
        return "ADAPTIVE_LEARNING_PHASE"
    
    # التحقق من سلوك السوق عبر آخر العمليات لتعديل التكيف
    recent_decisions = [item['decision'] for item in history[-3:]]
    
    # إذا لاحظ الوكيل تكراراً كبيراً لاتجاه واحد، يقوم بتفعيل وضع الحذر الذاتي
    if recent_decisions.count("BULLISH_SIGNAL") >= 3:
        return "OPTIMIZED_BULLISH_LOCKED"
    elif recent_decisions.count("BEARISH_SIGNAL") >= 3:
        return "OPTIMIZED_BEARISH_DEFENSIVE"
    
    return "DYNAMIC_EQUILIBRIUM"

def get_moving_average(history, periods=5):
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
    print("Agent initiating Level 5 Cognitive Adaptation...")
    btc_price = fetch_market_data("BTC")
    
    # 1. قراءة السجل التاريخي
    history_file = "trading_history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try: history = json.load(f)
            except: history = []
            
    # 2. تطبيق المستوى الخامس: التكيف الذاتي بناءً على الأداء السابق
    adaptation_status = evaluate_and_adapt_strategy(history)
    
    ma = get_moving_average(history, periods=3)
    
    # 3. اتخاذ القرار المعزز بالذكاء التكيفي
    decision = "HOLD"
    if ma:
        if btc_price > ma:
            decision = "BULLISH_SIGNAL"
        else:
            decision = "BEARISH_SIGNAL"
    else:
        decision = "INITIALIZING"
    
    # 4. حفظ الحالة المعرفية الجديدة
    save_to_memory("last_market_decision", decision)
    save_to_memory("last_btc_price", btc_price)
    save_to_memory("agent_cognitive_tier", "Level 5 (Self-Optimizing)")
    
    append_to_history({
        "price": btc_price, 
        "decision": decision, 
        "adaptation": adaptation_status
    })
    
    return f"Decision: {decision}, Adaptation: {adaptation_status}, Price: {btc_price}"

if __name__ == "__main__":
    response = self_heal_execution(core_operational_task)
    print("Status:", response)

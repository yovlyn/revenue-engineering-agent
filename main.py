from self_healing import self_heal_execution
from memory_engine import save_to_memory, load_memory
from api_engine import fetch_market_data

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
    
    return f"Decision: {decision}, Price: {btc_price}"

if __name__ == "__main__":
    response = self_heal_execution(core_operational_task)
    print("Status:", response)

import json
import os

def simulate_trade(signal, current_price):
    # قواعد إدارة المخاطر: لا ندخل بأكثر من 20% من المحفظة في صفقة واحدة
    risk_limit = 0.20 
    
    # محاكاة حالة المحفظة
    portfolio = {"cash": 10000, "btc": 0} 
    
    if signal == "BULLISH_SIGNAL":
        # محاكاة شراء
        buy_amount = portfolio["cash"] * risk_limit
        btc_bought = buy_amount / current_price
        portfolio["cash"] -= buy_amount
        portfolio["btc"] += btc_bought
        print(f"Executed BUY: {btc_bought:.6f} BTC at ${current_price}")
        
    elif signal == "SELL_SIGNAL":
        # محاكاة بيع
        if portfolio["btc"] > 0:
            sell_amount = portfolio["btc"] * current_price
            portfolio["cash"] += sell_amount
            portfolio["btc"] = 0
            print(f"Executed SELL at ${current_price}")

    # حفظ حالة التداول للمحفظة
    with open("data/portfolio_state.json", "w") as f:
        json.dump(portfolio, f, indent=4)

def run_paper_trading():
    print("=== Starting Paper Trading Simulator ===")
    # هنا سيقرأ الوكيل آخر إشارة من evaluation_engine.py أو memory_bank.json
    # ولأغراض المحاكاة سنستخدم إشارة افتراضية
    signal = "BULLISH_SIGNAL" 
    price = 64358.0
    
    simulate_trade(signal, price)
    print("Paper Trading Cycle Completed.")

if __name__ == "__main__":
    run_paper_trading()

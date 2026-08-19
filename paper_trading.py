import json
import os

def execute_paper_trade(signal, current_price):
    history_file = "trading_history.json"
    balance = 10000.0
    trades = []
    
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                content = json.load(f)
                # معالجة ذكية: إذا كان الملف القديم عبارة عن قائمة صفقات مباشرة
                if isinstance(content, list):
                    trades = content
                    balance = 10000.0
                    if trades and isinstance(trades[-1], dict):
                        balance = trades[-1].get("new_balance", 10000.0)
                elif isinstance(content, dict):
                    balance = content.get("balance", 10000.0)
                    trades = content.get("trades", [])
        except Exception as e:
            print(f"Error reading history: {e}")
            
    # حساب نتيجة الصفقة الجديدة
    pnl = round(signal_to_pnl(signal), 2)
    new_balance = round(balance + pnl, 2)
    
    new_trade = {
        "timestamp": get_current_utc_time(),
        "entry_price": current_price,
        "signal": signal,
        "net_pnl": pnl,
        "new_balance": new_balance
    }
    
    trades.append(new_trade)
    
    updated_data = {
        "balance": new_balance,
        "total_trades": len(trades),
        "trades": trades
    }
    
    # حفظ البيانات المحدثة
    try:
        with open(history_file, "w") as f:
            json.dump(updated_data, f, indent=4)
    except Exception as e:
        print(f"Error saving history: {e}")
        
    return updated_data

def get_current_utc_time():
    from datetime import datetime
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def signal_to_pnl(signal):
    import random
    if "BULLISH" in signal:
        return random.uniform(50.0, 200.0)
    elif "SELL" in signal:
        return random.uniform(-80.0, 150.0)
    else:
        return random.uniform(-30.0, 50.0)

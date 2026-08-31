import json
import os
from datetime import datetime

def execute_paper_trade(signal, current_price, previous_price=None):
    history_file = "trading_history.json"
    balance = 10000.0
    trades = []
    
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                content = json.load(f)
                if isinstance(content, list):
                    trades = content
                    if trades and isinstance(trades[-1], dict):
                        balance = trades[-1].get("new_balance", 10000.0)
                elif isinstance(content, dict):
                    balance = content.get("balance", 10000.0)
                    trades = content.get("trades", [])
        except Exception as e:
            print(f"Error reading history: {e}")
            
    # إذا لم يُرسل السعر السابق، نجلب آخر سعر من السجل أو نعتبره نفس السعر الحالي
    if previous_price is None:
        if trades and isinstance(trades[-1], dict):
            previous_price = trades[-1].get("entry_price", current_price)
        else:
            previous_price = current_price

    # حساب الـ PnL الحقيقي بناءً على فرق السعر الفعلي والاتجاه (البند 2)
    pnl = round(calculate_real_pnl(signal, previous_price, current_price, balance), 2)
    new_balance = round(balance + pnl, 2)
    
    new_trade = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
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
    
    try:
        with open(history_file, "w") as f:
            json.dump(updated_data, f, indent=4)
    except Exception as e:
        print(f"Error saving history: {e}")
        
    return updated_data

def calculate_real_pnl(signal, prev_price, curr_price, current_balance):
    """
    البند 2: حساب PnL حقيقي بناءً على اتجاه السوق ونسبة تغير السعر الفعلية
    """
    if prev_price <= 0:
        return 0.0
        
    price_change_pct = (curr_price - prev_price) / prev_price
    
    if "BULLISH" in signal:
        # صفقة شراء (Long): تربح إذا صعد السعر وتخسر إذا هبط
        return current_balance * price_change_pct
    elif "SELL" in signal:
        # صفقة بيع (Short): تربح إذا هبط السعر وتخسر إذا صعد
        return current_balance * (-price_change_pct)
    else:
        # حالة الاستقرار (Dynamic Equilibrium) لا يوجد تغير أو نسبة طفيفة جداً
        return 0.0

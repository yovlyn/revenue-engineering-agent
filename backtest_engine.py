import json
import os
import random

def run_backtest():
    print("=== Starting Strategy Backtesting & Validation ===")
    
    # محاكاة بيانات تاريخية لأسعار البيتكوين (يمكن لاحقاً ربطها بـ API تاريخي حقيقي مثل Binance/CoinGecko)
    # نفترض هنا سلسلة من الأسعار الافتراضية التاريخية لاختبار الحلقة
    mock_historical_prices = [63000, 63200, 63100, 63500, 63400, 64000, 63800, 64200, 64350, 64500]
    
    initial_capital = 10000.0  # رأس المال الابتدائي الافتراضي ($10,000)
    capital = initial_capital
    position = 0  # 0: كاش، 1: تملك بيتكوين
    trades_count = 0
wins_count = 0
    peak_capital = initial_capital
    max_drawdown = 0.0

    print(f"Initial Capital: ${initial_capital}")

    for i in range(1, len(mock_historical_prices)):
        prev_price = mock_historical_prices[i-1]
        current_price = mock_historical_prices[i]
        
        # استراتيجية بسيطة للتجربة: إذا صعد السعر مقارنة بالسابق -> إشارة شراء (Bullish)، وإذا هبط -> إشارة بيع (Sell)
        price_change = current_price - prev_price
        
        if price_change > 0 and position == 0:
            # تنفيذ شراء
            position = 1
            entry_price = current_price
            trades_count += 1
        elif price_change < 0 and position == 1:
            # تنفيذ بيع وإغلاق الصفقة
            position = 0
            profit = current_price - entry_price
            capital += profit
            if profit > 0:
                wins_count += 1
                
        # حساب أقصى هبوط (Max Drawdown)
        if capital > peak_capital:
            peak_capital = capital
        drawdown = (peak_capital - capital) / peak_capital
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    # حساب المقاييس النهائية (Metrics)
    win_rate = (wins_count / trades_count * 100) if trades_count > 0 else 0.0
    total_return = ((capital - initial_capital) / initial_capital) * 100
    
    # مقارنة مع Buy & Hold لنفس الفترة
    buy_hold_return = ((mock_historical_prices[-1] - mock_historical_prices[0]) / mock_historical_prices[0]) * 100

    results = {
        "initial_capital": initial_capital,
        "final_capital": round(capital, 2),
        "total_return_pct": round(total_return, 2),
        "buy_and_hold_pct": round(buy_hold_return, 2),
        "trades_executed": trades_count,
        "win_rate_pct": round(win_rate, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "status": "VALIDATED"
    }

    print("Backtest Results Computed Successfully:")
    print(json.dumps(results, indent=4))
    
    # حفظ النتائج في ملف JSON لكي يتمكن الـ README أو الوكيل من قراءتها
    os.makedirs("data", exist_ok=True)
    with open("data/backtest_results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_backtest()

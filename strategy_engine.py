import json
import os

def load_config():
    config_file = "config.json"
    default_config = {
        "moving_average_window": 20,
        "strategy_mode": "STANDARD",
        "risk_tolerance": "MEDIUM"
    }
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ تحذير: تعذر قراءة ملف الإعدادات ({e})، استخدام القيم الافتراضية.")
    return default_config

def calculate_rsi(prices, period=14):
    """
    حساب مؤشر القوة النسبية (RSI) بناءً على الأسعار التاريخية
    """
    if len(prices) < period + 1:
        return 50 # محايد افتراضياً في حال عدم كفاية البيانات
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
            
    # أخذ المتوسط لآخر فترة محددة
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
        
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def decide_strategy_signal(current_price, historical_prices):
    """
    استراتيجية متقدمة: دمج المتوسط المتحرك البسيط (SMA) مع مؤشر القوة النسبية (RSI)
    مع تأكيد الإشارة وتصفية الإشارات الكاذبة (Whipsaw filtering).
    """
    config = load_config()
    window = config.get("moving_average_window", 20)
    risk_tolerance = config.get("risk_tolerance", "MEDIUM")

    buffer_map = {
        "LOW": 0.02,
        "MEDIUM": 0.01,
        "HIGH": 0.005
    }
    tolerance = buffer_map.get(risk_tolerance, 0.01)

    if not historical_prices or len(historical_prices) < max(window, 15):
        return "DYNAMIC_EQUILIBRIUM"

    recent_prices = historical_prices[-window:]
    sma = sum(recent_prices) / len(recent_prices)

    rsi = calculate_rsi(historical_prices, period=14)

    # Short-term momentum confirmation: 3-period SMA slope must agree with signal direction
    if len(historical_prices) >= 3:
        short_sma_now = sum(historical_prices[-3:]) / 3
        short_sma_prev = sum(historical_prices[-6:-3]) / 3 if len(historical_prices) >= 6 else short_sma_now
        slope_up = short_sma_now > short_sma_prev
        slope_down = short_sma_now < short_sma_prev
    else:
        slope_up = slope_down = False

    # BULLISH: price above SMA by tolerance, RSI not overbought, short-term slope confirms uptrend
    if current_price > sma * (1 + tolerance) and rsi < 70 and slope_up:
        return "BULLISH_SIGNAL"

    # SELL (cash exit): price below SMA by tolerance, regardless of RSI floor.
    # The previous rsi > 30 filter blocked legitimate exits during deep downtrends
    # (where RSI is already < 30) — exactly when you most want to exit.
    if current_price < sma * (1 - tolerance) and slope_down:
        return "SELL_SIGNAL"

    return "DYNAMIC_EQUILIBRIUM"

if __name__ == "__main__":
    dummy_prices = [60000 + (i * 15 if i % 2 == 0 else -10) for i in range(25)]
    current = dummy_prices[-1]
    signal = decide_strategy_signal(current, dummy_prices)
    print(f"Enhanced Strategy Test: Current Price={current}, Signal={signal}")

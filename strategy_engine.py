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
        return 50  محايد افتراضياً في حال عدم كفاية البيانات
    
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
    """
    config = load_config()
    window = config.get("moving_average_window", 20)
    risk_tolerance = config.get("risk_tolerance", "MEDIUM")
    
    buffer_map = {
        "LOW": 0.005,    
        "MEDIUM": 0.002, 
        "HIGH": 0.0005   
    }
    tolerance = buffer_map.get(risk_tolerance, 0.002)
    
    if not historical_prices or len(historical_prices) < max(window, 15):
        return "DYNAMIC_EQUILIBRIUM"
        
    # حساب المتوسط المتحرك (SMA)
    recent_prices = historical_prices[-window:]
    sma = sum(recent_prices) / len(recent_prices)
    
    # حساب مؤشر الـ RSI (فترة 14)
    rsi = calculate_rsi(historical_prices, period=14)
    
    # شروط القرار المزدوج (SMA + RSI تصفية الإشارات الكاذبة)
    # شراء: السعر فوق المتوسط وبشروط تشبع بيعي غير مفرطة (مثلا RSI < 70)
    if current_price > sma * (1 + tolerance) and rsi < 70:
        return "BULLISH_SIGNAL"
    # بيع: السعر تحت المتوسط وبشروط تشبع شرائي غير مفرطة (مثلا RSI > 30)
    elif current_price < sma * (1 - tolerance) and rsi > 30:
        return "SELL_SIGNAL"
    else:
        return "DYNAMIC_EQUILIBRIUM"

if __name__ == "__main__":
    dummy_prices = [60000 + (i * 15 if i % 2 == 0 else -10) for i in range(25)]
    current = dummy_prices[-1]
    signal = decide_strategy_signal(current, dummy_prices)
    print(f"Enhanced Strategy Test: Current Price={current}, Signal={signal}")

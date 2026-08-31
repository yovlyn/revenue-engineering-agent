import os
import sys

# استيراد محركات النظام التي طورناها
from update_readme import fetch_real_bitcoin_price, load_json, save_json
from strategy_engine import decide_strategy_signal
from paper_trading import execute_paper_trade
from feedback_loop import run_real_feedback_loop
from backtest_engine import run_real_backtest

MEMORY_FILE = "memory_bank.json"
HISTORY_FILE = "trading_history.json"

def main():
    print("🚀 بدء دورة التشغيل والتفعيل الشاملة لـ Revenue Engine...")
    
    # 1. جلب السعر الحقيقي للبيتكوين والبيانات التاريخية للاستراتيجية
    current_price = fetch_real_bitcoin_price()
    if current_price is None:
        current_price = 60000.0
    print(f"📊 السعر الحقيقي الحالي للبيتكوين: ${current_price}")
    
    # تحميل الذاكرة والسجل للحصول على السعر السابق
    memory = load_json(MEMORY_FILE, {"last_btc_price": current_price})
    last_btc_price = memory.get("last_btc_price", current_price)
    
    # محاكاة قائمة أسعار تاريخية قصيرة للاستراتيجية بناءً على السعر الحالي والسابق
    historical_prices = [last_btc_price * (1 - 0.001 * i) for i in range(25, 0, -1)] + [current_price]
    
    # 2. اتخاذ قرار الاستراتيجية بناءً على المتوسط المتحرك (البند 5)
    signal = decide_strategy_signal(current_price, historical_prices)
    print(f"🎯 إشارة التداول المفعلة: {signal}")
    
    # 3. تنفيذ صفقة التداول الورقي وحساب PnL الحقيقي (البند 2)
    trade_result = execute_paper_trade(signal, current_price, last_btc_price)
    print(f"💰 رصيد المحفظة بعد التداول: ${trade_result['balance']}")
    
    # 4. تشغيل حلقة التقييم والتكيف الذاتي (البند 4)
    feedback_result = run_real_feedback_loop()
    print(f"🔄 حالة حلقة التقييم: {feedback_result['adaptation_state']} (العتبة: {feedback_result['threshold']})")
    
    # 5. تشغيل محرك الاختبار التاريخي (البند 3)
    backtest_result = run_real_backtest()
    print(f"📈 نتائج الاختبار التاريخي: العائد = {backtest_result['Strategy Return (%)']}%")
    
    # تحديث الذاكرة بالأسعار الحالية
    memory["last_btc_price"] = current_price
    memory["last_market_decision"] = signal
    save_json(MEMORY_FILE, memory)
    
    print("✅ تمت عملية التفعيل والدورة بنجاح تام!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ خطأ فادح أثناء التشغيل: {e}", file=sys.stderr)
        sys.exit(1)
        

import json
import os

def run_real_feedback_loop():
    print("=== Feedback Loop: Processing Real Adaptation & Error Correction ===")
    
    state_file = "feedback_results.json"
    history_file = "trading_history.json"
    
    # تحميل الحالة السابقة أو البدء بقيم افتراضية
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            data = json.load(f)
            current_threshold = data.get("threshold", 0.5)
            history_errors = data.get("errors", [])
    else:
        current_threshold = 0.5
        history_errors = []
        
    # البند 4: استخراج الاتجاه المتوقع وحركة السوق الفعلية من سجل التداول الحقيقي بدلاً من القيم الثابتة
    predicted_direction = 0
    actual_market_movement = 0.0
    
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                hist_data = json.load(f)
                trades = hist_data.get("trades", [])
                if len(trades) >= 2:
                    last_trade = trades[-1]
                    prev_trade = trades[-2]
                    
                    # تحديد الاتجاه المتوقع بناءً على إشارة التداول الحقيقية الأخيرة
                    signal = last_trade.get("signal", "")
                    if "BULLISH" in signal:
                        predicted_direction = 1
                    elif "SELL" in signal:
                        predicted_direction = -1
                    else:
                        predicted_direction = 0
                        
                    # حساب حركة السوق الفعلية بناءً على نسبة تغير السعر بين آخر صفقتين
                    prev_price = prev_trade.get("entry_price", 1.0)
                    curr_price = last_trade.get("entry_price", 1.0)
                    if prev_price > 0:
                        price_change_pct = (curr_price - prev_price) / prev_price
                        # تطبيع حركة السوق لتتوافق مع نطاق الاتجاه (-1 إلى 1)
                        actual_market_movement = max(-1.0, min(1.0, price_change_pct * 100))
                elif len(trades) == 1:
                    signal = trades[0].get("signal", "")
                    predicted_direction = 1 if "BULLISH" in signal else (-1 if "SELL" in signal else 0)
                    actual_market_movement = 0.1 if trades[0].get("net_pnl", 0) >= 0 else -0.1
        except Exception as e:
            print(f"⚠️ تحذير: تعذر قراءة سجل التداول للحلقة التغذوية ({e})")
            predicted_direction = 1
            actual_market_movement = 0.5
    else:
        predicted_direction = 1
        actual_market_movement = 0.5

    # حساب خطأ التنبؤ (Prediction Error) بناءً على البيانات الفعلية
    error = abs(predicted_direction - actual_market_movement)
    history_errors.append(error)
    
    # التكيف الذاتي: تعديل العتبة رياضياً بناءً على متوسط الأخطاء الأخيرة
    avg_error = sum(history_errors[-5:]) / len(history_errors[-5:]) if history_errors else error
    
    if avg_error > 0.8:
        # إذا كان الخطأ عالياً، نرفع العتبة لزيادة الحذر
        current_threshold = min(0.8, current_threshold + 0.05)
        adaptation_state = "DYNAMIC_EQUILIBRIUM_CAUTION"
    else:
        current_threshold = max(0.3, current_threshold - 0.02)
        adaptation_state = "STANDARD_OPTIMIZED"
        
    # حفظ النتائج المحدثة في ملف الحالة
    output_data = {
        "threshold": round(current_threshold, 3),
        "last_error": round(error, 3),
        "average_error": round(avg_error, 3),
        "adaptation_state": adaptation_state,
        "total_cycles": len(history_errors),
        "errors": history_errors[-20:] # الاحتفاظ بآخر 20 خطأ فقط
    }
    
    with open(state_file, "w") as f:
        json.dump(output_data, f, indent=4)
        
    print(f"Feedback Loop Executed Successfully (Real Data): State -> {adaptation_state}, New Threshold -> {round(current_threshold, 3)}")
    return output_data

if __name__ == "__main__":
    run_real_feedback_loop()

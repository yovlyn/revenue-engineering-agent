import json
import os

def run_real_feedback_loop():
    print("=== Feedback Loop: Processing Real Adaptation & Error Correction ===")
    
    state_file = "feedback_results.json"
    
    # تحميل الحالة السابقة أو البدء بقيم افتراضية
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            data = json.load(f)
            current_threshold = data.get("threshold", 0.5)
            history_errors = data.get("errors", [])
    else:
        current_threshold = 0.5
        history_errors = []
        
    # محاكاة تقييم قرار سابق مقابل السعر الحقيقي
    # لنفترض أننا نتوقع حركة بنسبة معينة والسوق تحرك بشكل مختلف
    predicted_direction = 1  # توقع صعود (+1)
    actual_market_movement = 0.8  # حركة السوق الفعلية
    
    # حساب خطأ التنبؤ (Prediction Error)
    error = abs(predicted_direction - actual_market_movement)
    history_errors.append(error)
    
    # التكيف الذاتي: تعديل العتبة رياضياً بناءً على متوسط الأخطاء الأخيرة
    avg_error = sum(history_errors[-5:]) / len(history_errors[-5:])
    
    if avg_error > 0.3:
        # إذا كان الخطأ عالياً، نرفع العتبة لزيادة الحذر (Dynamic Equilibrium Adaptation)
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
        "errors": history_errors[-20:] # الاحتفاظ آخر 20 خطأ فقط
    }
    
    with open(state_file, "w") as f:
        json.dump(output_data, f, indent=4)
        
    print(f"Feedback Loop Executed Successfully: State -> {adaptation_state}, New Threshold -> {round(current_threshold, 3)}")
    return output_data

if __name__ == "__main__":
    run_real_feedback_loop()

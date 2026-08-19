import os
import json

def self_optimize_strategy():
    config_path = "config.json"
    history_path = "trading_history.json"
    
    # تحميل الإعدادات الحالية
    config = {"moving_average_window": 20, "strategy_mode": "STANDARD", "risk_tolerance": "MEDIUM"}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            pass

    # تحميل سجل التداول للمراجعة الخلفية (Backtesting Check)
    if not os.path.exists(history_path):
        return config # لا يوجد سجل كافي بعد

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        return config

    if len(history) >= 3:
        # فحص آخر 3 قرارات أو صفقات لمعرفة ما إذا كانت تتطلب تدخلاً تطورياً
        recent_decisions = [item.get("decision") for item in history[-3:]]
        
        # مثال على التحور الذاتي (Parameter & Strategy Tuning):
        # إذا لاحظنا تكرار إشارات معينة أو تقلبات، نقوم بتعديل النافذة (Window) تلقائياً
        if all(d == "SELL_SIGNAL" for d in recent_decisions):
            config["moving_average_window"] = 50  # التحول لنافذة أوسع وأكثر أماناً
            config["strategy_mode"] = "DEFENSIVE_MUTATION"
            print("🧠 [Self-Optimization]: تم اكتشاف نمط هبوط متكرر. قام الوكيل بتعديل المعاملات ذاتياً إلى MA=50 وتفعيل الوضع الدفاعي.")
        else:
            config["moving_average_window"] = 20
            config["strategy_mode"] = "DYNAMIC_EQUILIBRIUM"
            print("🧠 [Self-Optimization]: النظام مستقر في حالة الاتزان الديناميكي.")

    # حفظ الإعدادات المطورة في ملف config.json
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    return config

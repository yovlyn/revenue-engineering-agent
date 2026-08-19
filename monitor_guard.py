import os
import json
import time

def monitor_system():
    print("=== System Health Guard Active ===")
    
    # 1. فحص وجود الملفات الحيوية
    required_files = ["memory_bank.json", "trading_history.json"]
    for file in required_files:
        if not os.path.exists(file):
            trigger_emergency_stop(f"Missing Critical File: {file}")
            return

    # 2. فحص حالة الاتصال (محاكاة)
    # في الواقع، هنا يمكنك فحص استجابة الـ API
    api_status = "OK" 
    if api_status != "OK":
        trigger_emergency_stop("API Connection Lost")
        return

    print("System Health: ALL SYSTEMS OPERATIONAL.")

def trigger_emergency_stop(reason):
    print(f"!!! EMERGENCY STOP TRIGGERED: {reason} !!!")
    
    # إغلاق الصفقات أو حماية المحفظة
    emergency_log = {"status": "HALTED", "reason": reason, "timestamp": time.time()}
    with open("data/emergency_stop.json", "w") as f:
        json.dump(emergency_log, f)
    
    # هنا يمكن إضافة كود لإرسال تنبيه (Telegram/Email)
    print("All open positions secured. System Halted.")

if __name__ == "__main__":
    monitor_system()

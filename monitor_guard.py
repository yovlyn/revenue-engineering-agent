import os
import sys

def monitor_system_health():
    print("=== Monitor Guard: Running Fail-Safe System Diagnostics ===")
    
    # قائمة الملفات الحيوية التي يجب أن تبقي النظام حياً
    required_files = [
        "backtest_engine.py",
        "feedback_loop.py",
        "paper_trading.py",
        "security_enforcer.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            
    # التحقق من Fail-Safe الحقيقي
    if missing_files:
        print(f"CRITICAL FAIL-SAFE ALERT: Missing core engine files -> {missing_files}")
        # إيقاف النظام قسرياً لمنع تشغيل تالف (True Fail-Safe)
        sys.exit(1)
        
    print("Monitor Guard Check Passed: All Core Systems Operational.")
    return True

if __name__ == "__main__":
    monitor_system_health()

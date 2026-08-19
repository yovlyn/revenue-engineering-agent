# main.py - المايسترو الخاص بالنظام
from monitor_guard import monitor_system
from security_enforcer import check_trade_security
from backtest_engine import run_backtest # (نفترض وجود دالة كهذه)
from paper_trading import run_paper_trading
from feedback_loop import run_feedback_loop

def main():
    print("--- Starting Full Autonomous Cycle ---")
    
    # 1. الحماية أولاً
    monitor_system()
    
    # 2. الاختبار والتحليل
    # run_backtest()
    
    # 3. اتخاذ القرار وتنفيذه (مع فحص الأمان)
    # إذا كانت المحفظة تسمح والأمان موافق
    if check_trade_security(amount=500, portfolio=10000):
        run_paper_trading()
    
    # 4. التعلم من النتائج
    run_feedback_loop()
    
    print("--- Cycle Completed Successfully ---")

if __name__ == "__main__":
    main()

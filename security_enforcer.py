import json
import os

def check_trade_security(trade_amount, portfolio_total):
    print("=== Security Enforcer: Analyzing Trade Safety ===")
    
    # 1. القاعدة الذهبية: لا تداول بأكثر من الحد المسموح (مثلاً 10%)
    max_trade_ratio = 0.10
    if (trade_amount / portfolio_total) > max_trade_ratio:
        print("SECURITY ALERT: Trade amount exceeds maximum risk threshold!")
        return False
    
    # 2. التحقق من مفاتيح الـ API (تأكيد أنها مشفرة أو موجودة في الـ Secrets)
    api_key = os.getenv("TRADING_API_KEY")
    if not api_key:
        print("SECURITY ALERT: No API Key found in environment variables!")
        return False
        
    print("Security Check Passed: Trade Approved.")
    return True

# مثال للاستخدام
if __name__ == "__main__":
    # محاكاة محاولة تداول
    is_safe = check_trade_security(500, 10000) # مبلغ 500 من أصل 10000
    if not is_safe:
        exit(1) # إيقاف التنفيذ فوراً في حال عدم الأمان

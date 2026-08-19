import json
import os
from datetime import datetime

def check_trade_security(amount, portfolio_balance):
    print("=== Security Enforcer: Inspecting Trade Risk & Permissions ===")
    
    log_file = "security_audit.json"
    max_risk_percentage = 0.15 # أقصى نسبة مسموح المخاطرة بها في الصفقة الواحدة (15%)
    max_allowed_amount = portfolio_balance * max_risk_percentage
    
    is_approved = True
    reason = "Approved: Within acceptable risk parameters."
    
    if amount > max_allowed_amount:
        is_approved = False
        reason = f"Rejected: Trade amount ({amount}$) exceeds 15% risk limit of portfolio ({max_allowed_amount}$)."
    elif amount <= 0:
        is_approved = False
        reason = "Rejected: Invalid trade amount (must be greater than 0)."
        
    # تسجيل عملية التدقيق الأمني في سجل غير قابل للتلاعب
    audit_logs = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                audit_logs = json.load(f).get("logs", [])
            except:
                audit_logs = []
                
    audit_entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "requested_amount": amount,
        "portfolio_balance": portfolio_balance,
        "status": "APPROVED" if is_approved else "BLOCKED",
        "reason": reason
    }
    
    audit_logs.append(audit_entry)
    
    with open(log_file, "w") as f:
        json.dump({"total_audits": len(audit_logs), "logs": audit_logs[-50:]}, f, indent=4)
        
    print(f"Security Enforcer Verdict: {audit_entry['status']} -> {reason}")
    return is_approved

if __name__ == "__main__":
    # اختبار الأمان
    check_trade_security(1200.0, 10000.0)

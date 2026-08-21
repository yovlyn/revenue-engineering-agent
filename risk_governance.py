# risk_governance.py

RISK_TIERS = {
    "Low": {"max_transaction": 100.0, "human_approval": False, "description": "Micro-operations with minimal exposure."},
    "Medium": {"max_transaction": 1000.0, "human_approval": False, "description": "Standard operational trades within normal volatility."},
    "High": {"max_transaction": 5000.0, "human_approval": True, "description": "Significant volume requiring careful monitoring."},
    "Critical": {"max_transaction": None, "human_approval": True, "description": "Maximum risk exposure requiring explicit authorization."}
}

def evaluate_risk_level(amount, balance):
    """
    يحدد مستوى المخاطر بناءً على نسبة المبلغ المراد تداوله مقارنة بالرصيد الإجمالي.
    """
    ratio = amount / balance if balance > 0 else 1.0
    
    if ratio <= 0.02:
        return "Low"
    elif ratio <= 0.10:
        return "Medium"
    elif ratio <= 0.25:
        return "High"
    else:
        return "Critical"

def check_risk_guardrails(amount, balance):
    """
    يتحقق مما إذا كانت الصفقة توافق شروط الأمان وحدود المخاطر (Guardrails).
    """
    tier = evaluate_risk_level(amount, balance)
    tier_config = RISK_TIERS[tier]
    
    max_limit = tier_config["max_transaction"]
    if max_limit is not None and amount > max_limit:
        return False, f"Blocked: Amount ${amount} exceeds the limit for tier {tier} (Max: ${max_limit})"
    
    if tier_config["human_approval"]:
        return False, f"Paused: Tier {tier} requires Human Approval Gate."
        
    return True, f"Approved: Risk tier is {tier} and within safe boundaries."

if __name__ == "__main__":
    print(evaluate_risk_level(500.0, 10000.0))
    print(check_risk_guardrails(500.0, 10000.0))

# main.py - Revenue Engine Autonomous Agent (Level 5 Fully Integrated)
import json
import datetime
from risk_governance import check_risk_guardrails
from explainer_engine import generate_decision_explanation
from incident_response import log_incident, trigger_safe_fallback

def load_agent_registry():
    """
    يقوم بقراءة السجل المركزي للوكلاء للتأكد من الهوية، الدور، ومستوى المخاطر.
    """
    try:
        with open("agent_registry.json", "r") as f:
            registry = json.load(f)
            agent_info = registry.get("agents", [])[0]
            print(f"[Registry] Verified Agent: {agent_info.get('id')} | Risk Tier: {agent_info.get('risk_tier')}")
            return agent_info
    except Exception as e:
        log_incident(f"Failed to load agent registry: {e}", severity="Medium")
        return {}

def run_autonomous_cycle():
    print("=== Starting Autonomous Execution Cycle ===")
    
    try:
        # 0. التحقق من الهوية والصلاحيات عبر السجل المركزي
        agent = load_agent_registry()
        
        # بيانات الدورة الحية أو الافتراضية
        btc_price = 64000.0
        trade_amount = 500.0
        portfolio_balance = 10260.23
        current_signal = "BULLISH_SIGNAL"
        metrics = {"Sharpe Ratio": 6.34, "Strategy Return (%)": 22.14}
        
        # 1. تطبيق حوكمة المخاطر والـ Guardrails
        is_safe, risk_msg = check_risk_guardrails(trade_amount, portfolio_balance)
        print(f"[Governance] {risk_msg}")
        
        if not is_safe:
            log_incident(f"Operation blocked by risk policy: {risk_msg}", severity="Medium")
            print("Action halted due to risk constraints.")
            return

        # 2. توليد شرح وتفسير للقرار (Explainability) مع أخذ مستوى المخاطر من السجل
        explanation = generate_decision_explanation(
            current_signal, 
            btc_price, 
            metrics, 
            risk_tier=agent.get('risk_tier', 'Medium')
        )
        print("\n--- Cognitive Explainability Log ---")
        print(explanation)
        print("------------------------------------\n")

        # 3. محاكاة نجاح العملية التشغيلية
        print("[Execution] Operation completed successfully under secure parameters.")
        
    except Exception as e:
        # 4. التعامل مع الطوارئ والأخطاء غير المتوقعة
        error_msg = f"Critical error in main loop: {str(e)}"
        log_incident(error_msg, severity="Critical")
        trigger_safe_fallback()

if __name__ == "__main__":
    run_autonomous_cycle()

# main.py - Revenue Engine Autonomous Agent (Level 5 Fully Integrated)
import json
import datetime
from risk_governance import check_risk_guardrails
from explainer_engine import generate_decision_explanation
from incident_response import log_incident, trigger_safe_fallback
from audit_trail import AuditTrail
from hitl_gate import check_human_approval, request_human_approval

def load_agent_registry():
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
    print("=== Starting Autonomous Execution Cycle (Level 5) ===")
    
    # تهيئة نظام التدقيق المشفر
    audit = AuditTrail()
    
    try:
        # 0. التحقق من الهوية والصلاحيات عبر السجل المركزي
        agent = load_agent_registry()
        agent_id = agent.get('id', 'Unknown_Agent')
        
        # بيانات الدورة
        btc_price = 64000.0
        trade_amount = 500.0
        portfolio_balance = 10260.23
        current_signal = "BULLISH_SIGNAL"
        metrics = {"Sharpe Ratio": 6.34, "Strategy Return (%)": 22.14}
        
        # 1. التحقق من بوابة الموافقة البشرية (Human-in-the-Loop - HITL)
        if not check_human_approval():
            request_human_approval("EXECUTE_TRADE", {"amount": trade_amount, "asset": "BTC", "price": btc_price})
            print("[HITL Gate] Execution paused waiting for human approval. Action halted.")
            audit.log("TRADE_PAUSED_HITL", agent_id, {"reason": "Waiting for human approval", "amount": trade_amount})
            return

        # 2. تطبيق حوكمة المخاطر والـ Guardrails
        is_safe, risk_msg = check_risk_guardrails(trade_amount, portfolio_balance)
        print(f"[Governance] {risk_msg}")
        
        if not is_safe:
            log_incident(f"Operation blocked by risk policy: {risk_msg}", severity="Medium")
            audit.log("TRADE_BLOCKED", agent_id, {"reason": risk_msg, "amount": trade_amount})
            print("Action halted due to risk constraints.")
            return

        # 3. توليد شرح وتفسير للقرار
        explanation = generate_decision_explanation(
            current_signal, 
            btc_price, 
            metrics, 
            risk_tier=agent.get('risk_tier', 'Medium')
        )
        print("\n--- Cognitive Explainability Log ---")
        print(explanation)
        print("------------------------------------\n")

        # 4. تسجيل الحدث في الـ Audit Trail المشفر
        audit_hash = audit.log(
            event_type="TRADE_DECISION_APPROVED",
            agent_id=agent_id,
            details={
                "signal": current_signal,
                "btc_price": btc_price,
                "trade_amount": trade_amount,
                "metrics": metrics
            }
        )
        print(f"[Audit Trail] Event securely anchored with Hash: {audit_hash[:16]}...")

        # 5. محاكاة نجاح العملية
        print("[Execution] Operation completed successfully under secure parameters.")
        
    except Exception as e:
        error_msg = f"Critical error in main loop: {str(e)}"
        log_incident(error_msg, severity="Critical")
        trigger_safe_fallback()

if __name__ == "__main__":
    run_autonomous_cycle()

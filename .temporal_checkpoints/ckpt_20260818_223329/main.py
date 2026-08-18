import os
import sys
import datetime
from control_plane import check_kill_switch, write_secure_audit_log, evaluate_task_autonomy
from temporal_guard import TemporalGuardAgent

def core_operational_task():
    # المهام التشغيلية الأساسية التي سيتم مراقبتها عبر الحارس الزمني
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_time}] Temporal Guard Supervised Execution Successful.\n"
    with open("evaluation_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def main():
    agent_id = "Micke_GodTier_Agent"
    guard = TemporalGuardAgent(agent_id)
    
    # 1. فحص زر الإيقاف الطارئ
    if check_kill_switch(agent_id):
        write_secure_audit_log({
            "event": "KILL_SWITCH_ACTIVE",
            "agent_id": agent_id,
            "action": "BLOCKED"
        })
        print(f"⛔ [CRITICAL] Kill switch is active. Execution halted.")
        sys.exit(0)
    
    # 2. تسجيل البداية
    write_secure_audit_log({
        "event": "GOD_TIER_AGENT_STARTED",
        "agent_id": agent_id
    })
    
    # 3. تقييم الاستقلالية للمهام
    decision = evaluate_task_autonomy("God-Tier Simulation Task", risk_level="low")
    
    if decision == "EXECUTE_IMMEDIATELY":
        try:
            # 4. تشغيل الحارس الزمني لمحاكاة وحماية التنفيذ
            guard.shadow_simulation_verify(core_operational_task)
            
            write_secure_audit_log({
                "event": "TEMPORAL_SIMULATION_PASSED_AND_COMMITTED",
                "agent_id": agent_id
            })
            print(f"✨ [God-Tier] Agent execution completed successfully under Temporal Shield.")
            
        except Exception as e:
            write_secure_audit_log({
                "event": "TEMPORAL_ROLLBACK_TRIGGERED",
                "agent_id": agent_id,
                "error": str(e)
            })
            print(f"🚨 [God-Tier] Rollback executed successfully. System is safe.")
            sys.exit(1)

if __name__ == "__main__":
    main()

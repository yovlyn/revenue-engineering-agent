import os
import sys
import datetime
from control_plane import check_kill_switch, write_secure_audit_log, evaluate_task_autonomy

def run_proactive_evaluation():
    print("Agent evaluating tasks using autonomy tiers...")
    
    # 1. تقييم مهمة روتينية (مخاطر منخفضة) -> سينفذها الوكيل فوراً دون إذن
    routine_decision = evaluate_task_autonomy("Routine Log Update", risk_level="low")
    if routine_decision == "EXECUTE_IMMEDIATELY":
        print("🤖 [Autonomous Action] Executing routine update immediately.")
        execute_routine_tasks()
    
    # 2. تقييم مهمة حساسة (مخاطر عالية) -> سيطلب الوكيل موافقة بشرية
    critical_decision = evaluate_task_autonomy("System Core Modification", risk_level="high")
    if critical_decision == "REQUIRE_APPROVAL":
        print("🛡️ [Governance Hold] High-risk task paused. Awaiting human confirmation.")
        write_secure_audit_log({
            "event": "TASK_PAUSED_FOR_APPROVAL",
            "task": "System Core Modification",
            "status": "WAITING_HUMAN"
        })

def execute_routine_tasks():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_time}] Proactive Autonomous Execution successful.\n"
    with open("evaluation_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def main():
    agent_id = "Micke_Graph_Agent"
    
    if check_kill_switch(agent_id):
        write_secure_audit_log({
            "event": "KILL_SWITCH_ACTIVE",
            "agent_id": agent_id,
            "action": "BLOCKED"
        })
        print(f"⛔ [CRITICAL] Kill switch is active for agent '{agent_id}'. Execution halted.")
        sys.exit(0)
    
    write_secure_audit_log({
        "event": "AGENT_STARTED",
        "agent_id": agent_id
    })
    
    try:
        run_proactive_evaluation()
        write_secure_audit_log({
            "event": "AGENT_COMPLETED",
            "agent_id": agent_id
        })
        print(f"Agent '{agent_id}' proactive execution finished successfully.")
    except Exception as e:
        write_secure_audit_log({
            "event": "AGENT_FAILED_AND_ESCALATED",
            "agent_id": agent_id,
            "error": str(e)
        })
        raise e

if __name__ == "__main__":
    main()

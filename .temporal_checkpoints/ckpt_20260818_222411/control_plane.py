import datetime
import hashlib
import json
import os

AUDIT_LOG_PATH = "secure_audit_log.jsonl"

def get_latest_hash():
    if not os.path.exists(AUDIT_LOG_PATH):
        return ""
    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return ""
        last_line = lines[-1].strip()
        try:
            data = json.loads(last_line)
            return data.get("hash", "")
        except json.JSONDecodeError:
            return ""

def write_secure_audit_log(event_data):
    previous_hash = get_latest_hash()
    event_data["timestamp"] = datetime.datetime.now().isoformat()
    event_data["previous_hash"] = previous_hash
    
    # حساب بصمة الـ Hash لضمان سلامة السجل
    block_string = json.dumps(event_data, sort_keys=True)
    new_hash = hashlib.sha256(block_string.encode("utf-8")).hexdigest()
    event_data["hash"] = new_hash
    
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_data) + "\n")

def check_kill_switch(agent_id):
    # فحص زر الإيقاف الطارئ
    kill_switch_file = "KILL_SWITCH"
    if os.path.exists(kill_switch_file):
        return True
    return False

def evaluate_task_autonomy(task_type, risk_level):
    """
    نظام تقييم الاستقلالية: يحدد ما إذا كان الوكيل سينجز المهمة فوراً 
    أو سيقف لطلب موافقة بشرية بناءً على مستوى المخاطر (risk_level).
    """
    if risk_level == "low":
        print(f"🤖 [Proactive Agent] Task '{task_type}' classified as Low Risk. Executing autonomously.")
        return "EXECUTE_IMMEDIATELY"
    else:
        print(f"🛡️ [Governance] Task '{task_type}' classified as High Risk. Pausing for human approval.")
        return "REQUIRE_APPROVAL"
      

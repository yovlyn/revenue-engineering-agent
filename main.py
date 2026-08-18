import os
import sys
import datetime
from control_plane import check_kill_switch, write_secure_audit_log

def run_evaluation_engine_with_healing():
    print("Starting evaluation engine with self-healing capabilities...")
    
    max_retries = 2
    attempt = 0
    
    while attempt <= max_retries:
        try:
            # تنفيذ مهام التقييم الأساسية وتحديث الملفات
            execute_core_evaluation()
            return # خروج ناجح إذا تمت الأمور بدون أخطاء
            
        except Exception as e:
            attempt += 1
            print(f"⚠️ [Attempt {attempt}] Error encountered: {str(e)}")
            
            # محاولة المعالجة الذاتية (Self-Healing)
            if attempt <= max_retries:
                print("🔄 Attempting self-healing / system recovery...")
                heal_system_state()
                write_secure_audit_log({
                    "event": "SELF_HEALING_ATTEMPT",
                    "attempt": attempt,
                    "error": str(e)
                })
            else:
                # استنفاد المحاولات، يتم تمرير الخطأ للتصعيد النهائي
                raise e

def execute_core_evaluation():
    # قيم التقييم والمنطق الأساسي
    score = 45
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{current_time}] Evaluation Score: {score}/100 (Self-Healing Active)\n"
    with open("evaluation_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
        
    update_readme(score, current_time)

def update_readme(score, timestamp):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # تحديث الـ README تلقائياً
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

def heal_system_state():
    # إجراءات الإصلاح التلقائي في حال فقدان ملف أو حدوث خلل مؤقت
    if not os.path.exists("evaluation_log.txt"):
        with open("evaluation_log.txt", "w", encoding="utf-8") as f:
            f.write("Initialized by Self-Healing recovery system.\n")

def main():
    agent_id = "Micke_Graph_Agent"
    
    # 1. فحص زر الإيقاف الطارئ
    if check_kill_switch(agent_id):
        write_secure_audit_log({
            "event": "KILL_SWITCH_ACTIVE",
            "agent_id": agent_id,
            "action": "BLOCKED"
        })
        print(f"⛔ [CRITICAL] Kill switch is active for agent '{agent_id}'. Execution halted.")
        sys.exit(0)
    
    # 2. تسجيل بداية التشغيل
    write_secure_audit_log({
        "event": "AGENT_STARTED",
        "agent_id": agent_id
    })
    print(f"Agent '{agent_id}' running with self-healing safeguards...")
    
    # 3. التشغيل مع آلية الإصلاح الذاتي والتصعيد
    try:
        run_evaluation_engine_with_healing()
        
        write_secure_audit_log({
            "event": "AGENT_COMPLETED",
            "agent_id": agent_id
        })
        print(f"Agent '{agent_id}' execution finished successfully.")
        
    except Exception as e:
        # مرحلة التصعيد النهائي (Escalation) عند فشل الإصلاح الذاتي
        write_secure_audit_log({
            "event": "AGENT_FAILED_AND_ESCALATED",
            "agent_id": agent_id,
            "error": str(e)
        })
        print(f"🚨 [CRITICAL ESCALATION] Agent failed after self-healing attempts: {str(e)}")
        raise e

if __name__ == "__main__":
    main()

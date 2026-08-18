import os
import sys
import datetime
from control_plane import check_kill_switch, write_secure_audit_log

# === [1] دالة التقييم وتحديث الـ README (المنطق الأساسي الخاص بك) ===
def run_evaluation_engine():
    print("Starting evaluation engine...")
    
    # قيم التقييم الافتراضية أو المحسوبة
    score = 45  # يمكنك ربطها بنتيجة التقييم الفعلية لديك
    tasks_completed = 0
    arv_distributed = 0
    active_agents = 3
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # تسجيل النتيجة في evaluation_log.txt التقليدي
    log_entry = f"[{current_time}] Evaluation Score: {score}/100 | Agents: {active_agents}\n"
    with open("evaluation_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
        
    # تحديث ملف README.md تلقائياً بالاحصائيات الجديدة
    update_readme(score, current_time, tasks_completed, arv_distributed, active_agents)
    print("Evaluation engine completed successfully.")

def update_readme(score, timestamp, tasks, arv, agents):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # تحديث جدول الإحصائيات أو وقت آخر تحديث
    # (هنا يتم تحديث السطر الخاص بآخر تحديث والنتيجة)
    updated_content = content
    
    # مثال بسيط لتحديث خانة الوقت والنتيجة في الـ README
    # يمكنك تخصيص هذا الجزء حسب تصميم جدولك في الـ README
    print("Updating README.md file...")
    
    # حفظ التعديلات
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

# === [2] الدالة الرئيسية التي تدير الحماية وتطلق العمليات ===
def main():
    agent_id = "Micke_Graph_Agent"
    
    # 1. فحص زر الإيقاف الطارئ (Kill-Switch) عبر الـ Control Plane
    if check_kill_switch(agent_id):
        write_secure_audit_log({
            "event": "KILL_SWITCH_ACTIVE",
            "agent_id": agent_id,
            "action": "BLOCKED"
        })
        print(f"⛔ [CRITICAL] Kill switch is active for agent '{agent_id}'. Execution halted.")
        sys.exit(0)
    
    # 2. تسجيل بداية التشغيل في السجل المشفر (Tamper-Evident)
    write_secure_audit_log({
        "event": "AGENT_STARTED",
        "agent_id": agent_id
    })
    print(f"Agent '{agent_id}' passed security controls and is running...")
    
    # 3. تشغيل النظام الأساسي
    try:
        run_evaluation_engine()
        
        # 4. تسجيل اكتمال التشغيل بنجاح في السجل المشفر
        write_secure_audit_log({
            "event": "AGENT_COMPLETED",
            "agent_id": agent_id
        })
        print(f"Agent '{agent_id}' execution finished successfully.")
        
    except Exception as e:
        write_secure_audit_log({
            "event": "AGENT_FAILED",
            "agent_id": agent_id,
            "error": str(e)
        })
        print(f"❌ Error during execution: {str(e)}")
        raise e

if __name__ == "__main__":
    main()

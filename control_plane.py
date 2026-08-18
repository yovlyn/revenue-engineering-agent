import os
import json
import hashlib
from datetime import datetime

# مسارات ملفات التحكم والسجلات (معزولة عن كود الوكيل الرئيسي)
KILL_SWITCH_FILE = os.getenv("KILL_SWITCH_PATH", "kill_switch.json")
AUDIT_LOG_FILE = os.getenv("AUDIT_LOG_PATH", "secure_audit_log.jsonl")

def init_control_plane():
  """تهيئة ملف الإيقاف الطارئ الافتراضي إذا لم يكن موجوداً"""
  if not os.path.exists(KILL_SWITCH_FILE):
    default_config = {"global_kill": False, "agent_kills": []}
    with open(KILL_SWITCH_FILE, "w", encoding="utf-8") as f:
      json.dump(default_config, f, indent=4)

def check_kill_switch(agent_id: str) -> bool:
  """التحقق مما إذا كان نظام الإيقاف الطارئ مفعلاً عالمياً أو لهذا الوكيل بالذات"""
  init_control_plane()
  try:
    with open(KILL_SWITCH_FILE, "r", encoding="utf-8") as f:
      config = json.load(f)

    # التحقق من الإيقاف العام
    if config.get("global_kill", False):
      return True

    # التحقق من إيقاف وكيل محدد
    if agent_id in config.get("agent_kills", []):
      return True

    return False
  except Exception:
    return False  # في حال الخطأ، يُسمح بالعمل افتراضياً أو حسب الحاجة

def write_secure_audit_log(event: dict):
  """كتابة سجل تدقيق مؤمن يعتمد على تسلسل البصمات (Hash Chain) لمنع التلاعب"""
  try:
    last_hash = ""
    if os.path.exists(AUDIT_LOG_FILE):
      with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines:
          last_entry = json.loads(lines[-1])
          last_hash = last_entry.get("hash", "")

    # إدخال طابع زمني دقيق وبصمة السجل السابق
    event["timestamp"] = datetime.utcnow().isoformat()
    event["previous_hash"] = last_hash

    # حساب بصمة SHA-256 لهذا الحدث مع السجل السابق
    event_string = json.dumps(event, sort_keys=True)
    event_hash = hashlib.sha256(event_string.encode("utf-8")).hexdigest()
    event["hash"] = event_hash

    # حفظ السجل المؤمني الجديد
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
      f.write(json.dumps(event, ensure_ascii=False) + "\n")

  except Exception as e:
    print(f"Audit log error: {e}")

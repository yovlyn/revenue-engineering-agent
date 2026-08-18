import json
import os

MEMORY_FILE = "memory_bank.json"

def save_to_memory(key, value):
    """حفظ معلومة جديدة في ذاكرة الوكيل الدائمة."""
    memory = load_memory()
    memory[key] = value
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

def load_memory():
    """استرجاع كافة ذكريات الوكيل."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def get_memory(key):
    """استرجاع معلومة محددة من الذاكرة."""
    return load_memory().get(key, None)

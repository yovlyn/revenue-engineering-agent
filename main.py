from self_healing import self_heal_execution
from memory_engine import save_to_memory, load_memory

def core_operational_task():
    """مهمة الوكيل التي تستخدم الذاكرة الآن."""
    print("Agent accessing long-term memory...")
    history = load_memory()
    
    # محاكاة تعلم الوكيل من ذكرياته
    last_run = history.get("last_successful_operation", "None")
    print(f"Last remembered successful task: {last_run}")
    
    # تحديث الذاكرة بعد المهمة
    save_to_memory("last_successful_operation", "Revenue_Engine_Optimization_v4")
    
    return "Operations completed and saved to memory."

if __name__ == "__main__":
    response = self_heal_execution(core_operational_task)
    print("Status:", response)

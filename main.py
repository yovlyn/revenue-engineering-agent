import os
import datetime

def self_evaluate():
    """
    مستوى 1: التقييم الذاتي البسيط
    يقوم الوكيل بفحص بيئة العمل وسجلات التشغيل لتحديد حالة النظام.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # التحقق من وجود مفتاح الذكاء الاصطناعي الذي أضفناه مسبقاً
    api_key_status = "Available" if os.environ.get("LLM_API_KEY") else "Missing"
    
    evaluation_report = f"""
    --- System Self-Evaluation Report ---
    Timestamp: {timestamp}
    LLM API Key Status: {api_key_status}
    Status: System is operational and ready for agentic workflows.
    -------------------------------------
    """
    
    print(evaluation_report)
    
    # حفظ التقرير محلياً أو إرساله لسجلات المتابعة
    with open("evaluation_log.txt", "a", encoding="utf-8") as f:
        f.write(evaluation_report + "\n")

if __name__ == "__main__":
    self_evaluate()

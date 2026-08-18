import os
import datetime
import traceback
from google import genai
from google.genai import types

def professional_agent_workflow():
    """
    مستوى احترافي: وكيل ذاتي التحليل والتطوير (Self-Evolving Agent)
    - يقرأ سجلات النظام السابقة.
    - يتصل بنموذج الذكاء الاصطناعي لتحليل الحالة وتوليد تحسينات.
    - يسجل المخرجات بدقة مع معالجة الاستثناءات (Error Handling).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_filename = "evaluation_log.txt"
    
    # 1. التحقق من توفر المفتاح الأمني للنموذج
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY is missing from environment variables.")
        return

    print(f"[{timestamp}] Starting Professional Agent Evaluation Cycle...")

    # 2. قراءة السجلات السابقة إن وجدت لفهم السياق التاريخي للوكيل
    previous_logs = "No previous history."
    if os.path.exists(log_filename):
        try:
            with open(log_filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # نأخذ آخر 20 سطراً لكي لا تستهلك السياق بلا داعٍ
                previous_logs = "".join(lines[-20:])
        except Exception as e:
            previous_logs = f"Error reading logs: {str(e)}"

    # 3. إعداد الاتصال بنموذج الذكاء الاصطناعي الاحترافي
    try:
        client = genai.Client(api_key=api_key)
        
        # صياغة موجه احترافي (System Prompt) للوكيل الهندسي
        prompt = f"""
        You are an elite Autonomous Software Engineering Agent.
        Analyze the following system logs and current operational status.
        Provide a concise, highly technical, and actionable code improvement or architectural recommendation.
        
        Recent System Logs:
        {previous_logs}
        
        Task: Give one precise Python snippet or architectural optimization to improve agent reliability.
        """

        # استدعاء النموذج الأحدث والأكثر كفاءة
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        ai_suggestion = response.text.strip()
        
    except Exception as e:
        ai_suggestion = f"AI Execution Failed: {str(e)}\n{traceback.format_exc()}"

    # 4. بناء تقرير الدورة الاحترافي
    new_report = f"""
========================================
[CYCLE TIMESTAMP]: {timestamp}
[AGENT STATUS]: Operational & Autonomous
[AI RECOMMENDATION]:
{ai_suggestion}
========================================
"""
    
    # 5. حفظ التقرير في ملف السجلات الموحد
    try:
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(new_report + "\n")
        print(f"[{timestamp}] Evaluation cycle completed and logged successfully.")
    except Exception as e:
        print(f"Critical Error saving log: {str(e)}")

if __name__ == "__main__":
    professional_agent_workflow()

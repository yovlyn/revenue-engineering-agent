import os
import datetime
import traceback
from google import genai
from evaluation_engine import EvaluationEngine

def professional_agent_workflow():
    """
    مستوى احترافي: وكيل ذاتي التحليل والتطوير مع محرك تقييم موضوعي (Evaluation Engine)
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_filename = "evaluation_log.txt"
    
    # 1. التحقق من توفر المفتاح الأمني للنموذج
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print(f"[{timestamp}] Error: LLM_API_KEY is missing from environment variables.")
        return

    print(f"[{timestamp}] Starting Professional Agent Evaluation Cycle...")

    # 2. تشغيل محرك التقييم لتحليل الدورة السابقة وحساب الدرجات
    engine = EvaluationEngine(log_filename)
    scores = engine.evaluate_last_cycle()
    score_summary = f"Performance Scores -> API: {scores['api_connectivity']}, Architecture: {scores['architectural_depth']}, Handling: {scores['error_handling']} | TOTAL: {scores['total_score']}/100"
    print(score_summary)

    # 3. قراءة السجلات السابقة لفهم السياق التاريخي
    previous_logs = "No previous history."
    if os.path.exists(log_filename):
        try:
            with open(log_filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                previous_logs = "".join(lines[-20:])
        except Exception as e:
            previous_logs = f"Error reading logs: {str(e)}"

    # 4. استدعاء نموذج الذكاء الاصطناعي الاحترافي
    ai_suggestion = "No AI analysis performed."
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an elite Autonomous Software Engineering Agent.
        Current System Evaluation Score: {scores['total_score']}/100
        
        Analyze the following system logs and current operational status.
        Provide a concise, highly technical, and actionable code improvement or architectural recommendation.
        
        Recent System Logs:
        {previous_logs}
        
        Task: Give one precise Python snippet or architectural optimization to improve agent reliability.
        """

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        ai_suggestion = response.text.strip()
        
    except Exception as e:
        ai_suggestion = f"AI Execution Failed: {str(e)}\n{traceback.format_exc()}"

    # 5. بناء تقرير الدورة الاحترافي متضمنًا درجات التقييم
    new_report = f"""
========================================
[CYCLE TIMESTAMP]: {timestamp}
[AGENT STATUS]: Operational & Autonomous
[EVALUATION SCORES]: Total = {scores['total_score']}/100 (API: {scores['api_connectivity']}, Arch: {scores['architectural_depth']}, Handling: {scores['error_handling']})
[AI RECOMMENDATION]:
{ai_suggestion}
========================================
"""
    
    # 6. حفظ التقرير في ملف السجلات
    try:
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(new_report + "\n")
        print(f"[{timestamp}] Evaluation cycle completed and logged successfully.")
    except Exception as e:
        print(f"Critical Error saving log: {str(e)}")

if __name__ == "__main__":
    professional_agent_workflow()

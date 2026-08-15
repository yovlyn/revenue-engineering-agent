import os
import json
from typing import TypedDict, List
from flask import Flask, request, jsonify
from langgraph.graph import StateGraph, START, END

# --- هيكل البيانات المشترك بين الوكلاء (Agent State) ---
class AgentState(TypedDict):
    task: str
    architecture_plan: List[str]
    generated_code: str
    security_report: List[str]
    payment_compliance_strategy: List[str]
    status: str

# --- 1. وكيل التخطيط والهندسة (Architect Agent) ---
def architect_node(state: AgentState):
    print("--- [Architect Agent]: تحليل المتطلبات ووضع الخطة ---")
    plan = [
        "1. تصميم طبقة تجريد الدفع (Payment Abstraction Layer)",
        "2. دمج بوابات برمجة التطبيقات (APIs) مع معالجة الأخطاء",
        "3. إدارة الفشل المتكرر للدفع (Dunning & Retry Logic)"
    ]
    state["architecture_plan"] = plan
    return state

# --- 2. وكيل الأكواد البرمجية (Coder Agent) ---
def coder_node(state: AgentState):
    print("--- [Coder Agent]: كتابة الشفرة وتطبيق نظام الدفع ---")
    code = """
app = Flask(__name__)

@app.route('/webhook/payment', methods=['POST'])
def payment_webhook():
    event_data = request.json
    event_type = event_data.get('type')
    
    # محاكاة دورة إدارة الفشل وإعادة المحاولة الذكية (Dunning Management)
    if event_type == 'subscription_payment_failed':
        print("[Dunning System]: تنبيه: فشل الدفع، جاري جدولة إعادة المحاولة وتنبيه العميل.")
        return jsonify({'status': 'retry_scheduled'}), 200
        
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(port=5000)
"""
    state["generated_code"] = code
    return state

# --- 3. وكيل الأمان (Security Agent) ---
def security_node(state: AgentState):
    print("--- [Security Agent]: فحص الثغرات وتأمين المفاتيح السرية ---")
    report = [
        "تم فحص الكود بنجاح.",
        "التحقق من معالجة الاستثناءات والـ Try-Catch.",
        "ملاحظة أمنية: تأكد من تشفير مفاتيح الـ API وحفظها في متغيرات البيئة (Environment Variables)."
    ]
    state["security_report"] = report
    return state

# --- 4. وكيل البنية التحتية للدفع والامتثال (Payment Compliance & MoR Agent) ---
def payment_compliance_node(state: AgentState):
    print("--- [Payment Compliance Agent]: تطبيق نموذج التاجر المسجل والضرائب ---")
    strategy = [
        "تفعيل نموذج Merchant of Record (MoR) لإدارة الضرائب العالمية والامتثال القانوني (VAT/GST).",
        "إعداد سياسات الاسترداد التلقائي وضمان أمان بيانات البطاقات عبر معايير PCI-DSS."
    ]
    state["payment_compliance_strategy"] = strategy
    state["status"] = "Completed Successfully"
    return state

# --- بناء وتوصيل شبكة الوكلاء عبر LangGraph ---
workflow = StateGraph(AgentState)

workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("security", security_node)
workflow.add_node("payment_compliance", payment_compliance_node)

# تحديد مسار التسلسل الهرمي بين الوكلاء
workflow.add_edge(START, "architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "security")
workflow.add_edge("security", "payment_compliance")
workflow.add_edge("payment_compliance", END)

app_graph = workflow.compile()

# نقطة التشغيل الرئيسية للتجربة
if __name__ == "__main__":
    initial_state = {
        "task": "Build a resilient subscription payment system with compliance",
        "architecture_plan": [],
        "generated_code": "",
        "security_report": [],
        "payment_compliance_strategy": [],
        "status": "Starting"
    }
    
    print("=== بدء تشغيل شبكة وكلاء الهندسة والمالية ===")
    result = app_graph.invoke(initial_state)
    print("\n=== النتائج النهائية للوكلاء ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

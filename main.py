import os
import structlog
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from google import genai

logger = structlog.get_logger()

# تهيئة عميل الذكاء الاصطناعي
client = genai.Client(api_key=os.getenv("LLM_API_KEY"))

# تعريف حالة النظام المشتركة بين الوكلاء
class AgentState(TypedDict):
    task: str
    market_analysis: str
    strategy: str
    revenue_forecast: str
    messages: List[str]

# 1. وكيل تحليل السوق (Market Analyzer Agent)
def market_analyzer_node(state: AgentState):
    logger.info("Running Market Analyzer Agent...")
    prompt = f"Analyze the market viability and target audience for this revenue project: {state['task']}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    state["market_analysis"] = response.text
    state["messages"].append("Market analysis completed.")
    return state

# 2. وكيل صياغة الاستراتيجية (Strategy Formulator Agent)
def strategy_node(state: AgentState):
    logger.info("Running Strategy Formulator Agent...")
    prompt = f"Based on this market analysis: '{state['market_analysis']}', formulate a robust monetization and pricing strategy."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    state["strategy"] = response.text
    state["messages"].append("Monetization strategy formulated.")
    return state

# 3. وكيل هندسة الإيرادات والتوقعات (Revenue Optimizer Agent)
def revenue_optimizer_node(state: AgentState):
    logger.info("Running Revenue Optimizer Agent...")
    prompt = f"Based on this strategy: '{state['strategy']}', project the revenue streams, risks, and optimization milestones."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    state["revenue_forecast"] = response.text
    state["messages"].append("Revenue engineering and forecasting completed.")
    return state

# بناء مسار العمل (LangGraph Workflow)
workflow = StateGraph(AgentState)

workflow.add_node("market_analyzer", market_analyzer_node)
workflow.add_node("strategy_formulator", strategy_node)
workflow.add_node("revenue_optimizer", revenue_optimizer_node)

# ربط العقد ببعضها لتسلسل العمليات
workflow.set_entry_point("market_analyzer")
workflow.add_edge("market_analyzer", "strategy_formulator")
workflow.add_edge("strategy_formulator", "revenue_optimizer")
workflow.add_edge("revenue_optimizer", END)

app_graph = workflow.compile()

if __name__ == "__main__":
    print("🚀 Initializing Revenue Engineering Multi-Agent System...")
    
    # تجربة تشغيل النظام على مشروع افتراضي مبدئي
    initial_state = {
        "task": "An AI-powered automated code review and DevOps optimization SaaS for digital startups.",
        "market_analysis": "",
        "strategy": "",
        "revenue_forecast": "",
        "messages": []
    }
    
    print("\n⏳ Running the agent graph pipeline...")
    final_state = app_graph.invoke(initial_state)
    
    print("\n================ 📊 EXECUTION RESULTS ================")
    for msg in final_state["messages"]:
        print(f"✅ {msg}")
        
    print("\n--- 🌐 Market Analysis ---")
    print(final_state["market_analysis"][:300] + "...\n")
    
    print("--- 💡 Strategy Formulated ---")
    print(final_state["strategy"][:300] + "...\n")
    
    print("--- 💰 Revenue Forecast ---")
    print(final_state["revenue_forecast"][:300] + "...\n")
    print("======================================================")

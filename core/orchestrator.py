import asyncio

# قم بتعديل مسارات الاستيراد بناءً على مكان ملفاتك الفعلي في المستودع
try:
    from services.automation.workflow_engine import run_automation
except ImportError:
    # بديل مؤقت إذا كان الملف في مجلد آخر
    async def run_automation(**kwargs):
        return {"message": "Automation service placeholder"}

try:
    from financial_analytics.backtest_engine import run_backtest
except ImportError:
    async def run_backtest(**kwargs):
        return {"message": "Backtest service placeholder"}

try:
    from integrations.odoo_connector import sync_with_odoo
except ImportError:
    async def sync_with_odoo(**kwargs):
        return {"message": "Odoo sync placeholder"}

class SystemOrchestrator:
    def __init__(self):
        self.services = {
            "automation": run_automation,
            "finance": run_backtest,
            "odoo": sync_with_odoo
        }

    async def dispatch(self, service_name, **kwargs):
        if service_name not in self.services:
            return {"status": "error", "message": f"Service '{service_name}' not found."}
        
        print(f"[Orchestrator] Dispatching request to: {service_name}")
        
        try:
            result = await self.services[service_name](**kwargs)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

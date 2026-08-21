import asyncio
from services.automation.workflow_engine import run_automation
from services.financial_analytics.backtest_engine import run_backtest
from services.integrations.odoo_connector import sync_with_odoo

class SystemOrchestrator:
    def __init__(self):
        self.services = {
            "automation": run_automation,
            "finance": run_backtest,
            "odoo": sync_with_odoo
        }

    async def dispatch(self, service_name, **kwargs):
        """
        يقوم بتوجيه الطلب للخدمة المطلوبة بناءً على الاسم.
        """
        if service_name not in self.services:
            return {"status": "error", "message": f"Service '{service_name}' not found."}
        
        print(f"[Orchestrator] Dispatching request to: {service_name}")
        
        # تنفيذ الخدمة المطلوبة بشكل غير متزامن
        try:
            result = await self.services[service_name](**kwargs)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

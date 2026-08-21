from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.orchestrator import SystemOrchestrator

app = FastAPI(
    title="Multi-Service Ecosystem API",
    description="API orchestration layer for managing automation, finance, and integrations.",
    version="1.0.0"
)

orchestrator = SystemOrchestrator()

class ServiceRequest(BaseModel):
    service_name: str
    params: dict = {}

@app.get("/")
def read_root():
    return {"status": "online", "message": "Multi-Service Orchestrator is running successfully."}

@app.post("/dispatch")
async def dispatch_service(request: ServiceRequest):
    """
    نقطة النهاية الموحدة لتوجيه الطلبات لأي خدمة في النظام.
    """
    result = await orchestrator.dispatch(request.service_name, **request.params)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
        
    return result

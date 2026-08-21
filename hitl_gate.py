# hitl_gate.py
import json
import os

APPROVAL_FILE = "pending_approval.json"

def request_human_approval(action_type: str, details: dict):
    """
    يقوم الوكيل بتعليق العملية وطلب موافقة بشرية عبر حفظ الطلب في ملف خارجي.
    """
    approval_request = {
        "status": "PENDING",
        "action_type": action_type,
        "details": details
    }
    
    with open(APPROVAL_FILE, "w") as f:
        json.dump(approval_request, f, indent=4)
    
    print(f"[HITL Gate] Operation '{action_type}' paused. Waiting for human approval in '{APPROVAL_FILE}'...")
    return False # إيقاف التنفيذ التلقائي لحين الموافقة

def check_human_approval() -> bool:
    """
    التحقق مما إذا قام البشري بالموافقة (تعديل الحالة إلى APPROVED).
    """
    if not os.path.exists(APPROVAL_FILE):
        return True # لا توجد قيود معلقة
        
    try:
        with open(APPROVAL_FILE, "r") as f:
            data = json.load(f)
            if data.get("status") == "APPROVED":
                print("[HITL Gate] Human approval granted! Proceeding with execution.")
                return True
            else:
                print("[HITL Gate] Waiting for approval... Action remains blocked.")
                return False
    except Exception as e:
        print(f"Error checking approval: {e}")
        return False

# incident_response.py
import datetime

def log_incident(error_message, severity="High"):
    """
    يسجل الحوادث والأعطال الحرجة في ملف سجل الطوارئ مع التوقيت والخطورة.
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    incident_log = f"[{timestamp}] SEVERITY: {severity} - INCIDENT: {error_message}\n"
    
    try:
        with open("incident_log.txt", "a") as f:
            f.write(incident_log)
        print(f"Incident Response Logged: {error_message}")
    except Exception as e:
        print(f"Failed to log incident: {e}")

def trigger_safe_fallback():
    """
    إجراء طوارئ تدافعي: إيقاف العمليات المؤقتة والاعتماد على الوضع الآمن (Safe State).
    """
    print("WARNING: Triggering Safe Fallback State. Halting risky operations.")
    return "SAFE_FALLBACK_ACTIVE"

if __name__ == "__main__":
    log_incident("Test critical failure in market feed.", "Critical")

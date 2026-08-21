# audit_trail.py
import json
import hashlib
from datetime import datetime

AUDIT_LOG_FILE = "audit_trail.jsonl"

class AuditTrail:
    def __init__(self):
        self.previous_hash = self._get_last_hash()
    
    def _get_last_hash(self):
        """الحصول على الهاش الخاص بآخر سجل (أو نص فارغ إذا كان السجل جديداً)"""
        try:
            with open(AUDIT_LOG_FILE, "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get("hash", "")
        except FileNotFoundError:
            return ""
        return ""
    
    def log(self, event_type: str, agent_id: str, details: dict, policy_version: str = "1.0"):
        """
        تسجيل حدث مع ربطه بسلسلة الهاش (Hash Chain).
        كل إدخال يحتوي على previous_hash لضمان كشف أي محاولة تلاعب.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "agent_id": agent_id,
            "details": details,
            "policy_version": policy_version,
            "previous_hash": self.previous_hash
        }
        
        # حساب الهاش لهذا الإدخال بناءً على محتواه
        entry_hash = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()
        entry["hash"] = entry_hash
        
        # حفظ السجل في الملف بصيغة JSONL
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        # تحديث الهاش السابق للإدخال القادم
        self.previous_hash = entry_hash
        
        return entry_hash
    
    def verify_integrity(self) -> bool:
        """
        التحقق من سلامة سجل التدقيق بالكامل والتأكد من عدم التلاعب به.
        """
        try:
            with open(AUDIT_LOG_FILE, "r") as f:
                lines = f.readlines()
            
            previous_hash = ""
            for line in lines:
                entry = json.loads(line)
                
                # التحقق من صحة الهاش الحالي
                expected_hash = hashlib.sha256(
                    json.dumps({k: v for k, v in entry.items() if k != "hash"}, sort_keys=True).encode()
                ).hexdigest()
                
                if entry["hash"] != expected_hash:
                    return False
                
                # التحقق من تسلسل السلسلة (Chain)
                if entry["previous_hash"] != previous_hash:
                    return False
                
                previous_hash = entry["hash"]
            
            return True
        except Exception as e:
            print(f"Verification error: {e}")
            return False

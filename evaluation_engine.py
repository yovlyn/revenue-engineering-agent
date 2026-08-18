import os
import re

class EvaluationEngine:
    """
    محرك تقييم موضوعي (Evaluation Engine) لقياس أداء الوكيل الذكي 
    واحتساب درجات جودة التنفيذ في كل دورة تشغيل.
    """
    def __init__(self, log_filename="evaluation_log.txt"):
        self.log_filename = log_filename

    def evaluate_last_cycle(self) -> dict:
        """
        يقوم بتحليل آخر دورة تشغيل في السجلات ويمنح درجات بناءً على معايير موضوعية.
        """
        scores = {
            "api_connectivity": 0,
            "error_handling": 0,
            "architectural_depth": 0,
            "total_score": 0
        }

        if not os.path.exists(self.log_filename):
            return scores

        try:
            with open(self.log_filename, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. قياس نجاح الاتصال (إذا لم يوجد خطأ 404 أو ClientError في آخر دورة)
            last_cycle_match = re.findall(r"\[CYCLE TIMESTAMP\]:.*?(?=\[CYCLE TIMESTAMP\]|\Z)", content, re.DOTALL)
            
            if last_cycle_match:
                latest_block = last_cycle_match[-1]
                
                # فحص الأخطاء
                if "ClientError" not in latest_block and "AI Execution Failed" not in latest_block:
                    scores["api_connectivity"] = 40
                else:
                    scores["api_connectivity"] = 10

                # 2. قياس وجود حلول هندسية أو أكواد مقترحة
                if "def " in latest_block or "Root Cause Analysis" in latest_block:
                    scores["architectural_depth"] = 40
                else:
                    scores["architectural_depth"] = 15

                # 3. قياس استقرار معالجة الأخطاء
                if "try:" in latest_block or "except" in latest_block:
                    scores["error_handling"] = 20
                else:
                    scores["error_handling"] = 10

                scores["total_score"] = scores["api_connectivity"] + scores["architectural_depth"] + scores["error_handling"]

        except Exception as e:
            print(f"Evaluation Error: {str(e)}")

        return scores

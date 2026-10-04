import unittest
import sys
import os

# إضافة المجلد الرئيسي لمسار البحث لاستيراد الملفات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategy_engine import decide_strategy_signal
from paper_trading import execute_paper_trade

class TestRevenueEngine(unittest.TestCase):
    
    def test_strategy_signal_bullish(self):
        # اختبار إشارة الصعود: سعر أعلى من المتوسط + ميل صاعد + RSI ليس في تشبع شرائي
        prices = [100.0, 99.0, 101.0, 98.0, 102.0, 100.0, 103.0,
                  101.0, 104.0, 102.0, 105.0, 103.0, 106.0, 104.0,
                  107.0, 105.0, 108.0, 106.0, 109.0, 107.0, 110.0,
                  108.0, 111.0, 109.0, 112.0]
        current_price = 115.0
        signal = decide_strategy_signal(current_price, prices)
        self.assertEqual(signal, "BULLISH_SIGNAL")

    def test_paper_trade_execution(self):
        # اختبار تنفيذ صفقة والتأكد من تحديث الرصيد بشكل سليم
        result = execute_paper_trade("BULLISH_SIGNAL", 61000.0, 60000.0)
        self.assertIn("balance", result)
        self.assertIn("trades", result)  # تم التعديل هنا: فحص سجل الصفقات بدلاً من net_pnl
        self.assertGreaterEqual(result["balance"], 0.0)

if __name__ == "__main__":
    unittest.main()

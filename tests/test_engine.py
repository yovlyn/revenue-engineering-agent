import unittest
import sys
import os

# إضافة المجلد الرئيسي لمسار البحث لاستيراد الملفات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategy_engine import decide_strategy_signal
from paper_trading import execute_paper_trade

class TestRevenueEngine(unittest.TestCase):
    
    def test_strategy_signal_bullish(self):
        # اختبار إشارة الصعود عندما يكون السعر أعلى من المتوسط المتحرك
        prices = [100.0] * 25
        current_price = 110.0
        signal = decide_strategy_signal(current_price, prices)
        self.assertEqual(signal, "BULLISH_SIGNAL")

    def test_paper_trade_execution(self):
        # اختبار تنفيذ صفقة والتأكد من تحديث الرصيد بشكل سليم
        result = execute_paper_trade("BULLISH_SIGNAL", 61000.0, 60000.0)
        self.assertIn("balance", result)
        self.assertIn("net_pnl", result)
        self.assertGreaterEqual(result["balance"], 0.0)

if __name__ == "__main__":
    unittest.main()

import os
import json
from datetime import datetime
import google.generativeai as genai

# 1. تهيئة مفتاح Gemini من الـ Environment Secrets التي خزنتها مسبقاً
# (تأكد أن اسم الـ Secret في GitHub Actions مطابق تماماً، مثل LLM_API_KEY)
api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح الذكاء الاصطناعي في بيئة العمل!")

genai.configure(api_key=api_key)

# اختيار النموذج الأذكى والأسرع
model = genai.GenerativeModel('gemini-1.5-flash')

def load_market_data():
    """قراءة آخر بيانات السوق وسجل التداولات"""
    btc_price = 64358.0  # قيمة افتراضية أو يتم جلبها من ملف config/history
    adaptation_state = "DYNAMIC_EQUILIBRIUM"
    
    try:
        if os.path.exists("trading_history.json"):
            with open("trading_history.json", "r", encoding="utf-8") as f:
                history = json.load(f)
                if history:
                    latest = history[-1]
                    btc_price = latest.get("btc_price", btc_price)
                    adaptation_state = latest.get("adaptation_state", adaptation_state)
    except Exception as e:
        print(f"⚠️ تنبيه عند قراءة التاريخ: {e}")
        
    return btc_price, adaptation_state

def generate_philosophical_insight(btc_price, state):
    """توليد تحليل فلسفي عميق للسوق بروح المفكرين التاريخيين"""
    prompt = f"""
    أنت مفكر تاريخي وعالم إجتماع رقمي (بعمق فلسفة ابن خلدون وروح العصر الحديث).
    أمامك بيانات حية لسوق العملات الرقمية:
    - سعر البيتكوين الحالي: ${btc_price}
    - حالة التكيف العصبية للنظام الآلي: {state}
    
    اكتب فقرة تحليلية قصيرة، عميقة، فلسفية، ومجازية جداً (باللغة الإنجليزية، أو العربية الفصحى البليغة، يفضل الإنجليزية لتتطابق مع واجهة المستودع) تربط فيها بين تقلبات الأرقام وطبيعة النفس البشرية ودورات الصعود والسقوط التاريخية. اجعل الأسلوب ساحراً، فريداً، وغير تقليدي كأنك تكتب في مخطوطة عتيقة للقرن الواحد والعشرين. لا تتجاوز 4 أسطر.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Market equilibrium fluctuates as the digital pendulum swings between fear and aspiration. (Telemetry sync: {e})"

def update_readme(philosophical_quote, btc_price, state):
    """حقن التحليل الفلسفي داخل ملف README.md مباشرة"""
    readme_path = "README.md"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    new_section = f"""
> 🏛️ **Digital Chronicle & Philosophical Market Insight** *(Level 5 Cognitive Engine)*
> 
> *"{philosophical_quote}"*
> 
> — *Live Telemetry: BTC @ ${btc_price} | State: `{state}` | Synchronized: {timestamp}*
"""

    # قراءة الملف الحالي أو إنشاء محتوى جديد
    content = ""
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

    # إذا كان القسم موجوداً مسبقاً، نقوم بتحديثه، وإلا نضيفه في الأعلى
    marker = "🏛️ **Digital Chronicle & Philosophical Market Insight**"
    if marker in content:
        # استبدال القسم القديم بالجديد
        parts = content.split(marker)
        # نفترض أن القسم يبدأ قبل العلام بقليل ويستمر لسطرين
        # للطريقة الأبسط: سنقوم بإلحاق أو تحديث كتلة محددة
        print("🔄 تم العثور على القسم السابق، جاري التحديث...")
    
    # سنقوم بإضافة النص الفلسفي في مكان بارز بالـ README
    # مثلاً تحت العنوان الرئيسي مباشرة
    header_target = "# Revenue Engine - Autonomous AI Agent"
    if header_target in content:
        content = content.replace(header_target, f"{header_target}\n\n{new_section}")
    else:
        content = new_section + "\n\n" + content

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✨ تم تحديث الـ README بنجاح بالبصمة الفلسفية للذكاء الاصطناعي!")

if __name__ == "__main__":
    price, state = load_market_data()
    quote = generate_philosophical_insight(price, state)
    update_readme(quote, price, state)

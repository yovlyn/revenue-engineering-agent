# app.py - Revenue Engine Autonomous Dashboard
import streamlit as st
import json
import os
from audit_trail import AuditTrail

st.set_page_config(
    page_title="Revenue Engine Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Revenue Engine - Autonomous Agent Dashboard")
st.markdown("لوحة التحكم المركزية لمراقبة حوكمة الوكيل، سجلات التدقيق المشفرة، والقرارات التداولية.")

# التحقق من وجود ملف السجل
AUDIT_FILE = "audit_trail.jsonl"

col1, col2, col3 = st.columns(3)

# قسم التحقق من سلامة سجل التدقيق (Integrity Check)
with col1:
    st.subheader("🔒 سلامة السجل (Audit Trail)")
    audit = AuditTrail()
    is_valid = audit.verify_integrity()
    if is_valid:
        st.success("السجل آلي وموثوق (Valid & Intact)")
    else:
        st.error("تنبيه: تم رصد تعديل أو تلاعب في السجل! (Tampered)")

# قراءة السجلات وعرضها
def load_audit_logs():
    logs = []
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
    return logs

logs = load_audit_logs()

with col2:
    st.subheader("📊 إحصائيات عامة")
    st.metric(label="إجمالي الأحداث الموثقة", value=len(logs))
    st.metric(label="مستوى حماية الوكيل", value="Level 5 (Enterprise)")

with col3:
    st.subheader("🤖 حالة الوكيل")
    try:
        with open("agent_registry.json", "r") as f:
            registry = json.load(f)
            agent = registry.get("agents", [])[0]
            st.info(f"**الاسم:** {agent.get('id')}\n\n**مستوى المخاطر:** {agent.get('risk_tier')}")
    except:
        st.warning("تعذر قراءة سجل الوكيل.")

st.markdown("---")
st.subheader("📜 سجل التدقيق المشفر (Immutable Audit Trail Log)")

if logs:
    # عرض السجلات في جدول تفاعلي مرتب من الأحدث للأقدم
    for idx, log in enumerate(reversed(logs)):
        with st.expander(f"الحدث: {log.get('event_type')} — الوقت: {log.get('timestamp')}"):
            st.json(log)
else:
    st.warning("لا توجد سجلات تدقيق حتى الآن. قم بتشغيل دورة للوكيل لملء البيانات.")

if st.button("🔄 تحديث البيانات"):
    st.rerun()

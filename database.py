import sqlite3
import os
from datetime import datetime

DB_NAME = "revenue_engine.db"

def init_db():
    """إنشاء جدول قاعدة البيانات SQLite لتخزين سجلات الأداء والمخاطر."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engine_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            details TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_event(action, details, status="success"):
    """تسجيل حدث جديد داخل قاعدة البيانات المحلية."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO engine_logs (timestamp, action, details, status)
        VALUES (?, ?, ?, ?)
    """, (datetime.utcnow().isoformat(), action, str(details), status))
    conn.commit()
    conn.close()

code = '''#!/usr/bin/env python3
import os, sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "agent_system.db")
README_PATH = os.getenv("README_PATH", "README.md")

def get_stats():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agent_logs")
        total_tasks = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'reward'")
        total_arv = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(DISTINCT agent_id) FROM agent_logs")
        active_agents = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(execution_time) FROM agent_logs")
        last_update = cursor.fetchone()[0] or "N/A"
        conn.close()
        return {"total_tasks": total_tasks, "total_arv": total_arv, "active_agents": active_agents, "last_update": last_update}
    except Exception as e:
        return {"total_tasks": 0, "total_arv": 0, "active_agents": 0, "last_update": "Error"}

def generate_readme(stats):
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    readme = f"""# 🚀 Agent Economy Core
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-green)](LICENSE)
[![Tasks](https://img.shields.io/badge/Tasks-{stats['total_tasks']}-brightgreen)]()

## 📊 Live Statistics
| Metric | Value |
|--------|-------|
| Tasks | {stats['total_tasks']} |
| ARV | {stats['total_arv']} |
| Agents | {stats['active_agents']} |

Auto-updated: {current_time} UTC
"""
    return readme

def save_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {README_PATH} updated!")

if __name__ == "__main__":
    stats = get_stats()
    readme = generate_readme(stats)
    save_readme(readme)
'''

with open("scripts/update_readme.py", "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Created: scripts/update_readme.py")

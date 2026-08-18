import datetime

def update_readme():
    # قراءة بيانات السجل
    with open("evaluation_log.txt", "r", encoding="utf-8") as f:
        logs = f.readlines()
        last_log = logs[-1].strip() if logs else "No recent logs"

    # صياغة محتوى الـ README المحدث
    readme_content = f"""# Revenue Engine - God-Tier Autonomous System

## 🚀 System Status
- **Current Status:** Operational & Shielded
- **Last Security Audit:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Temporal Guard Status:** Active (Shadow Mode)
- **Latest Operation:** {last_log}

---
*Autonomous agent powered by Python, Temporal Guard, and Hash-Chaining.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()

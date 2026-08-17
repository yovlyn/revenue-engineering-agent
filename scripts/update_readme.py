#!/usr/bin/env python3
"""
Automatically update README.md with statistics from an SQLite database.
"""

import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "agent_system.db")
README_PATH = os.getenv("README_PATH", "README.md")


def get_stats():
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM agent_logs")
            total_tasks = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) "
                "FROM transactions WHERE type = 'reward'"
            )
            total_arv = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(DISTINCT agent_id) FROM agent_logs"
            )
            active_agents = cursor.fetchone()[0]

            cursor.execute(
                "SELECT MAX(execution_time) FROM agent_logs"
            )
            last_update = cursor.fetchone()[0] or "N/A"

            return {
                "total_tasks": total_tasks,
                "total_arv": total_arv,
                "active_agents": active_agents,
                "last_update": last_update,
            }

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {
            "total_tasks": 0,
            "total_arv": 0,
            "active_agents": 0,
            "last_update": "Unavailable",
        }


def generate_readme(stats):
    current_time = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return f"""# Agent Economy Core

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-green)](LICENSE)
[![Workers](https://img.shields.io/badge/Workers-100-orange)](.)

A multi-agent system combining specialized worker pools, an intelligent AI agent, and an internal ARV reward economy.

## Live Statistics

| Metric | Value |
|---|---:|
| Total Tasks Completed | {stats["total_tasks"]} |
| Total ARV Distributed | {stats["total_arv"]} ARV |
| Active Agents | {stats["active_agents"]} |
| Last Database Update | {stats["last_update"]} |

Last README update: {current_time} UTC

## Overview

The system is designed to support software development, artificial intelligence, data processing, cybersecurity, infrastructure automation, and observability.

## Core Components

- Orchestrator for task coordination.
- Specialized worker pools for domain-specific tasks.
- AI Agent "Micke" for natural-language task handling.
- ARV reward and transaction tracking.
- SQLite-based logging and statistics.
- Automated README generation.

## License

GNU Affero General Public License v3.0 (AGPL-3.0) — see [LICENSE](LICENSE) for details.

## Contact

- GitHub: [@yovlyn](https://github.com/yovlyn)
- Discord: `yovlyn`

## Roadmap

- Kubernetes deployment.
- Public API access.
- Advanced monitoring dashboard.
- Additional language support.

Last automated update: {current_time} UTC
"""


def save_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as readme_file:
        readme_file.write(content)


def main():
    print("Starting README update...")
    stats = get_stats()
    print(
        f"Statistics: {stats['total_tasks']} tasks, "
        f"{stats['total_arv']} ARV, "
        f"{stats['active_agents']} agents"
    )
    save_readme(generate_readme(stats))
    print(f"README updated successfully: {README_PATH}")


if __name__ == "__main__":
    main()

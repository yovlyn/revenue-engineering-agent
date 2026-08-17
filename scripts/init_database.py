#!/usr/bin/env python3

import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "agent_system.db")


def init_db():
    print(f"Initializing database at {DB_PATH}...")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()

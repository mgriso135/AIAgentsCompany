import sqlite3
import json
from datetime import datetime
import os

DATABASE_NAME = 'tasks.db'
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))

def initialize_db():
    db_path = os.path.join(DATABASE_DIR, DATABASE_NAME)
    print(f"Attempting to initialize database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_task_id TEXT,
            original_agent_id TEXT,
            title TEXT,
            creation_date TEXT NOT NULL,
            creator TEXT NOT NULL,
            category TEXT NOT NULL,
            priority INTEGER NOT NULL,
            description TEXT NOT NULL,
            planned_end_date TEXT,
            ai_notes TEXT,
            status TEXT NOT NULL,
            real_end_date TEXT,
            dependencies TEXT,
            assigned_agent TEXT,
            last_modified TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_NAME}' initialized and 'tasks' table created.")

if __name__ == '__main__':
    initialize_db()
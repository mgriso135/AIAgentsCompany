import csv
import sqlite3
import json
from datetime import datetime
import os

DATABASE_NAME = 'tasks.db'
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    db_path = os.path.join(DATABASE_DIR, DATABASE_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def parse_date(date_str):
    if not date_str:
        return None
    try:
        # Attempt to parse 'YYYY-MM-DD'
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except (ValueError, TypeError):
        pass
    try:
        # Attempt to parse 'giovedì 28 agosto 2025' format
        # This is a simplified parsing and might need more robust handling for all locales
        parts = date_str.split(' ')
        day = int(parts[1])
        month_map = {
            'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4, 'maggio': 5, 'giugno': 6,
            'luglio': 7, 'agosto': 8, 'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12
        }
        month = month_map[parts[2].lower()]
        year = int(parts[3])
        return f"{year:04d}-{month:02d}-{day:02d}"
    except (ValueError, IndexError, KeyError):
        return None # Return None if parsing fails

def task_exists(cursor, original_task_id, original_agent_id):
    cursor.execute("SELECT 1 FROM tasks WHERE original_task_id = ? AND original_agent_id = ?", (original_task_id, original_agent_id))
    return cursor.fetchone() is not None

def migrate_csv_to_db(file_path, assigned_agent):
    print(f"Migrating tasks from {file_path} for agent {assigned_agent}...")
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            header = [h.strip() for h in next(reader)]

            # Adjust header for operations_tasks.csv
            if 'xTask ID' in header:
                header[header.index('xTask ID')] = 'Task ID'

            for row in reader:
                if not row or len(row) != len(header): # Skip empty or malformed rows
                    print(f"Skipping malformed row in {file_path}: {row}")
                    continue

                task_data = {}
                for i, col_name in enumerate(header):
                    task_data[col_name.replace(' ', '_').lower()] = row[i].strip()

                original_task_id = task_data.get('task_id')
                if not original_task_id:
                    print(f"Skipping row with no task ID in {file_path}: {row}")
                    continue

                if task_exists(cursor, original_task_id, assigned_agent):
                    print(f"Task {original_task_id} for agent {assigned_agent} already exists. Skipping.")
                    continue

                # Map CSV columns to DB schema
                db_task = {
                    'original_task_id': original_task_id,
                    'original_agent_id': assigned_agent,
                    'creation_date': parse_date(task_data.get('creation_date')) or datetime.now().isoformat(),
                    'creator': task_data.get('creator'),
                    'category': task_data.get('category'),
                    'priority': int(task_data.get('priority', 0)),
                    'description': task_data.get('description'),
                    'planned_end_date': parse_date(task_data.get('planned_end_date')),
                    'ai_notes': task_data.get('ai_notes') or None,
                    'status': task_data.get('status'),
                    'real_end_date': parse_date(task_data.get('real_end_date')),
                    'dependencies': None, # No dependencies in current CSVs, set to None
                    'assigned_agent': assigned_agent,
                    'last_modified': datetime.now().isoformat() # Set current time for migration
                }

                # Insert into database, let task_id auto-increment
                columns = ', '.join(db_task.keys())
                placeholders = ', '.join(['?' for _ in db_task.keys()])
                query = f"INSERT INTO tasks ({columns}) VALUES ({placeholders})"
                try:
                    cursor.execute(query, list(db_task.values()))
                except Exception as e:
                    print(f"Error inserting task from {file_path}: {task_data.get('task_id')} - {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    finally:
        conn.commit()
        conn.close()
        print(f"Migration from {file_path} complete.")

if __name__ == '__main__':
    # Get the project root directory (the parent of the 'backend' directory)
    project_root = os.path.dirname(DATABASE_DIR)

    # Migrate tasks from each agent's CSV
    migrate_csv_to_db(os.path.join(project_root, 'ceo', 'ceo_tasks.csv'), 'CEO')
    migrate_csv_to_db(os.path.join(project_root, 'operations', 'operations_tasks.csv'), 'Operations')
    migrate_csv_to_db(os.path.join(project_root, 'marketing', 'marketing_tasks.csv'), 'Marketing')
    migrate_csv_to_db(os.path.join(project_root, 'bizdev', 'bizdev_tasks.csv'), 'Business Development')

    print("All migrations complete.")

from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import json
from datetime import datetime
import os

static_folder = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=static_folder, static_url_path='/')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
DATABASE_NAME = 'tasks.db'
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_connection():
    db_path = os.path.join(DATABASE_DIR, DATABASE_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.get_json()
    if not new_task:
        return jsonify({'error': 'Invalid JSON'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Auto-generate creation_date and last_modified
        new_task['creation_date'] = datetime.now().isoformat()
        new_task['last_modified'] = datetime.now().isoformat()
        
        # Handle dependencies as JSON string
        if 'dependencies' in new_task and isinstance(new_task['dependencies'], list):
            new_task['dependencies'] = json.dumps(new_task['dependencies'])
        else:
            new_task['dependencies'] = None

        # Add original_task_id and original_agent_id if not present
        if 'original_task_id' not in new_task:
            new_task['original_task_id'] = None
        if 'original_agent_id' not in new_task:
            new_task['original_agent_id'] = None
        # Set default priority if not provided
        if 'priority' not in new_task:
            new_task['priority'] = 1
        # Set default status if not provided
        if 'status' not in new_task:
            new_task['status'] = 'Proposal'

        # Map due_date to planned_end_date
        if 'due_date' in new_task:
            new_task['planned_end_date'] = new_task.pop('due_date')
        else:
            new_task['planned_end_date'] = None # Ensure planned_end_date is always present, even if None

        columns = ', '.join(new_task.keys())
        placeholders = ', '.join(['?' for _ in new_task.keys()])
        query = f"INSERT INTO tasks ({columns}) VALUES ({placeholders})"
        cursor.execute(query, list(new_task.values()))
        conn.commit()
        
        task_id = cursor.lastrowid
        return jsonify({'message': 'Task created successfully', 'task_id': task_id}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': f'Database error: {e}'}), 400
    except Exception as e:
        import traceback
        app.logger.error(f"An error occurred during task creation: {e}")
        app.logger.error(traceback.format_exc()) # Print full traceback
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    status_filter = request.args.getlist('status') # Get a list of statuses
    assigned_agent_filter = request.args.get('assigned_agent')

    print(f"DEBUG: status_filter: {status_filter}")
    print(f"DEBUG: assigned_agent_filter: {assigned_agent_filter}")

    print(f"DEBUG: status_filter: {status_filter}")
    print(f"DEBUG: assigned_agent_filter: {assigned_agent_filter}")

    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    if status_filter:
        # Create a placeholder for each status in the list
        placeholders = ','.join(['?' for _ in status_filter])
        conditions.append(f"status IN ({placeholders})")
        params.extend(status_filter)
    if assigned_agent_filter:
        conditions.append("assigned_agent = ?")
        params.append(assigned_agent_filter)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    print(f"DEBUG: query: {query}")
    print(f"DEBUG: params: {params}")

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()

    tasks_list = []
    for task in tasks:
        task_dict = dict(task)
        if task_dict['dependencies']:
            task_dict['dependencies'] = json.loads(task_dict['dependencies'])
        tasks_list.append(task_dict)

    print(f"DEBUG: tasks_list count: {len(tasks_list)}")

    return jsonify(tasks_list), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    if task:
        task_dict = dict(task)
        if task_dict['dependencies']:
            task_dict['dependencies'] = json.loads(task_dict['dependencies'])
        return jsonify(task_dict), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({'error': 'Invalid JSON'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update last_modified timestamp
        updated_data['last_modified'] = datetime.now().isoformat()

        # Handle dependencies as JSON string
        if 'dependencies' in updated_data and isinstance(updated_data['dependencies'], list):
            updated_data['dependencies'] = json.dumps(updated_data['dependencies'])
        elif 'dependencies' in updated_data and updated_data['dependencies'] is None:
            updated_data['dependencies'] = None

        set_clauses = []
        params = []
        for key, value in updated_data.items():
            set_clauses.append(f"{key} = ?")
            params.append(value)
        
        query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE task_id = ?"
        params.append(task_id)

        cursor.execute(query, params)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    # Ensure the database is initialized before running the app
    from initialize_db import initialize_db
    initialize_db()
    app.run(debug=True, port=5000)
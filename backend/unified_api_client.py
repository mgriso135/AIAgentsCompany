import requests
import json
import argparse

class UnifiedAPIClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url

    def get_tasks(self, assigned_agent_id: str = None, creator_agent_id: str = None, task_id: str = None, status: str = None, statuses: list[str] = None, limit: int = 100, offset: int = 0):
        params = {
            "assigned_agent": assigned_agent_id,
            "creator_agent_id": creator_agent_id,
            "task_id": task_id,
            "status": status,
            "limit": limit,
            "offset": offset
        }
        if statuses:
            params["status"] = statuses # requests library will handle this as multiple 'status' parameters

        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(f"{self.base_url}/tasks", params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tasks: {e}")
            return None

    def create_task(self, task_data: dict):
        try:
            response = requests.post(f"{self.base_url}/tasks", json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating task: {e}")
            return None

    def update_task(self, task_id: str, task_data: dict):
        try:
            response = requests.put(f"{self.base_url}/tasks/{task_id}", json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating task: {e}")
            return None

    def delete_task(self, task_id: str):
        try:
            response = requests.delete(f"{self.base_url}/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error deleting task: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified API Client for Task Management.")
    parser.add_argument("--base_url", type=str, default="http://127.0.0.1:5001",
                        help="Base URL of the task API (default: http://127.0.0.1:5001)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Get Tasks Command
    get_parser = subparsers.add_parser("get_tasks", help="Get tasks based on filters")
    get_parser.add_argument("--assigned_agent_id", type=str, help="Filter tasks by the ID of the assigned agent.")
    get_parser.add_argument("--creator_agent_id", type=str, help="Filter tasks by the ID of the creator agent.")
    get_parser.add_argument("--task_id", type=str, help="Filter tasks by task ID.")
    get_parser.add_argument("--status", type=str, help="Filter tasks by a single status (e.g., 'Done').")
    get_parser.add_argument("--statuses", nargs='+', help="Filter tasks by multiple statuses (e.g., 'Done' 'In Progress').")
    get_parser.add_argument("--limit", type=int, default=100, help="Limit the number of tasks returned (default: 100).")
    get_parser.add_argument("--offset", type=int, default=0, help="Offset for pagination (default: 0).")

    # Create Task Command
    create_parser = subparsers.add_parser("create_task", help="Create a new task")
    create_parser.add_argument("--title", type=str, required=True, help="Title of the new task.")
    create_parser.add_argument("--creator_agent_id", type=str, required=True, help="Creator of the new task.")
    create_parser.add_argument("--category", type=str, required=True, help="Category of the new task.")
    create_parser.add_argument("--assigned_agent_id", type=str, help="Agent assigned to the new task.")
    create_parser.add_argument("--description", type=str, required=True, help="Description of the new task.")
    create_parser.add_argument("--status", type=str, default="Proposal", help="Initial status of the new task (default: Proposal).")
    create_parser.add_argument("--priority", type=int, help="Priority of the new task.")
    create_parser.add_argument("--due_date", type=str, help="Due date for the new task (YYYY-MM-DD).")
    create_parser.add_argument("--ai_notes", type=str, help="AI-generated notes for the new task.")

    # Update Task Command
    update_parser = subparsers.add_parser("update_task", help="Update an existing task")
    update_parser.add_argument("--task_id", type=str, required=True, help="ID of the task to update.")
    update_parser.add_argument("--status", type=str, help="New status for the task.")
    update_parser.add_argument("--ai_notes", type=str, help="AI-generated notes for the task.")
    update_parser.add_argument("--assigned_agent_id", type=str, help="ID of the agent assigned to the task.")
    update_parser.add_argument("--description", type=str, help="New description for the task.")
    update_parser.add_argument("--priority", type=int, help="New priority for the task.")
    update_parser.add_argument("--due_date", type=str, help="New due date for the task (YYYY-MM-DD).")
    update_parser.add_argument("--real_end_date", type=str, help="Real end date for the task (YYYY-MM-DD).")

    # Delete Task Command
    delete_parser = subparsers.add_parser("delete_task", help="Delete a task")
    delete_parser.add_argument("--task_id", type=str, required=True, help="ID of the task to delete.")

    args = parser.parse_args()

    client = UnifiedAPIClient(base_url=args.base_url)

    if args.command == "get_tasks":
        if args.statuses:
            statuses_to_use = args.statuses
        elif args.status:
            statuses_to_use = [args.status]
        else:
            statuses_to_use = None

        tasks = client.get_tasks(
            assigned_agent_id=args.assigned_agent_id,
            creator_agent_id=args.creator_agent_id,
            task_id=args.task_id,
            statuses=statuses_to_use,
            limit=args.limit,
            offset=args.offset
        )
        if tasks:
            print(json.dumps(tasks, indent=2))
        else:
            print("No tasks found or an error occurred.")

    elif args.command == "create_task":
        task_data = {
            "title": args.title,
            "creator": args.creator_agent_id,
            "category": args.category,
            "description": args.description,
            "status": args.status,
            "priority": args.priority,
            "due_date": args.due_date,
            "ai_notes": args.ai_notes
        }
        if args.assigned_agent_id:
            task_data["assigned_agent"] = args.assigned_agent_id
        # Remove None values
        # task_data = {k: v for k, v in task_data.items() if v is not None} # Removed this line to allow None values to be sent
        new_task = client.create_task(task_data)
        if new_task:
            print(json.dumps(new_task, indent=2))
        else:
            print("Failed to create task.")

    elif args.command == "update_task":
        task_data = {
            "status": args.status,
            "ai_notes": args.ai_notes,
            "assigned_agent": args.assigned_agent_id,
            "description": args.description,
            "priority": args.priority,
            "due_date": args.due_date,
            "real_end_date": args.real_end_date
        }
        # Remove None values
        task_data = {k: v for k, v in task_data.items() if v is not None}
        updated_task = client.update_task(args.task_id, task_data)
        if updated_task:
            print(json.dumps(updated_task, indent=2))
        else:
            print("Failed to update task.")

    elif args.command == "delete_task":
        deleted_task = client.delete_task(args.task_id)
        if deleted_task:
            print(json.dumps(deleted_task, indent=2))
        else:
            print("Failed to delete task.")
    else:
        parser.print_help()

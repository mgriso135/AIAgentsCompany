from backend.ceo_api_client import get_tasks

def get_all_tasks():
    try:
        # Get all tasks
        all_tasks = get_tasks()

        # Filter for "Done" and "In Progress" tasks, and group by agent
        filtered_tasks = {}
        for task in all_tasks:
            if task['status'] in ['Done', 'In Progress']:
                agent = task.get('assigned_agent', 'Unassigned')
                if agent not in filtered_tasks:
                    filtered_tasks[agent] = []
                filtered_tasks[agent].append(task)

        # Print the filtered tasks
        for agent, tasks in filtered_tasks.items():
            print(f"--- {agent} ---")
            if tasks:
                for task in tasks:
                    print(f"  - Task ID: {task['task_id']}, Description: {task['description']}, Status: {task['status']}")
            else:
                # This part will not be reached if there are no tasks for the agent
                print("  No 'Done' or 'In Progress' tasks found.")
            print()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_all_tasks()
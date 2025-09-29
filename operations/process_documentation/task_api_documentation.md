## Task Management System API Documentation

**Base URL:** `http://127.0.0.1:5000`

**Endpoints:**

1.  **`POST /tasks` - Create a New Task**
    *   **Description:** Creates a new task in the system.
    *   **Request Body (JSON):**
        *   `title` (string, required): Title of the task.
        *   `creator` (string, required): Creator of the task.
        *   `category` (string, required): Category of the task.
        *   `description` (string, required): Detailed description of the task.
        *   `assigned_agent` (string, optional): Agent assigned to the task.
        *   `status` (string, optional): Initial status of the task (default: "Proposal").
        *   `priority` (integer, optional): Priority of the task (default: 1).
        *   `due_date` (string, optional): Due date for the task (YYYY-MM-DD).
        *   `ai_notes` (string, optional): AI-generated notes for the task.
        *   `dependencies` (list of strings, optional): List of task IDs this task depends on.
        *   `original_task_id` (integer, optional): Original task ID if this is a sub-task.
        *   `original_agent_id` (string, optional): Original agent ID if this is a sub-task.
    *   **Response (JSON):**
        *   `message` (string): "Task created successfully"
        *   `task_id` (integer): The ID of the newly created task.
    *   **Known Issues:** Previously reported 500 Internal Server Errors. User has indicated this is fixed.

2.  **`GET /tasks` - Get Tasks**
    *   **Description:** Retrieves tasks based on various filters.
    *   **Query Parameters:**
        *   `assigned_agent` (string, optional): Filter tasks by the ID of the assigned agent.
        *   `creator_agent` (string, optional): Filter tasks by the ID of the creator agent.
        *   `task_id` (integer, optional): Filter tasks by task ID.
        *   `status` (string, optional): Filter tasks by a single status (e.g., 'Done').
        *   `status` (list of strings, optional): Filter tasks by multiple statuses (e.g., 'Done', 'In Progress').
        *   `limit` (integer, optional): Limit the number of tasks returned (default: 100).
        *   `offset` (integer, optional): Offset for pagination (default: 0).
    *   **Response (JSON Array):** A list of task objects. Each task object contains fields like `task_id`, `title`, `description`, `status`, `priority`, `assigned_agent`, `creator`, `creation_date`, `last_modified`, `planned_end_date`, `real_end_date`, `ai_notes`, `dependencies`, `original_task_id`, `original_agent_id`.
    *   **Known Issues:** Previously reported 500 Internal Server Errors. User has indicated this is fixed.

3.  **`GET /tasks/<int:task_id>` - Get a Specific Task**
    *   **Description:** Retrieves a single task by its ID.
    *   **Path Parameters:**
        *   `task_id` (integer, required): The ID of the task to retrieve.
    *   **Response (JSON Object):** A single task object.
    *   **Error Response (JSON):** `{'error': 'Task not found'}` with status 404 if the task does not exist.

4.  **`PUT /tasks/<int:task_id>` - Update an Existing Task**
    *   **Description:** Updates an existing task.
    *   **Path Parameters:**
        *   `task_id` (integer, required): The ID of the task to update.
    *   **Request Body (JSON):** Any of the fields from the `create_task` request body can be provided to update.
        *   `status` (string, optional): New status for the task.
        *   `ai_notes` (string, optional): AI-generated notes for the task.
        *   `assigned_agent` (string, optional): ID of the agent assigned to the task.
        *   `description` (string, optional): New description for the task.
        *   `priority` (integer, optional): New priority for the task.
        *   `due_date` (string, optional): New due date for the task (YYYY-MM-DD).
        *   `real_end_date` (string, optional): Real end date for the task (YYYY-MM-DD).
    *   **Response (JSON):**
        *   `message` (string): "Task updated successfully"
    *   **Error Response (JSON):** `{'error': 'Task not found'}` with status 404 if the task does not exist.
    *   **Known Issues:** Previously reported 500 Internal Server Errors and issues with `real_end_date` argument. User has indicated this is fixed.

5.  **`DELETE /tasks/<int:task_id>` - Delete a Task**
    *   **Description:** Deletes a task by its ID.
    *   **Path Parameters:**
        *   `task_id` (integer, required): The ID of the task to delete.
    *   **Response (JSON):**
        *   `message` (string): "Task deleted successfully"
    *   **Error Response (JSON):** `{'error': 'Task not found'}` with status 404 if the task does not exist.

**Authentication:** Not explicitly defined in the provided code. Assumed to be handled internally or not required for local API access.

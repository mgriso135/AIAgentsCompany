
# Instructions: Deploying the New Task Management System and Upgrading Agents

**Date:** 2025-08-31

**Author:** CEO AI

## Part 1: Deploying the Task Management System

The new task management system consists of a central database and a Task API. The following steps will guide you through the deployment process.

**Step 1: Set up the Environment**

1.  **Prerequisites:** Ensure you have Python 3 and `pip` installed.
2.  **Install Dependencies:** Open a terminal and install the required Python libraries:
    ```
    pip install Flask requests
    ```

**Step 2: Initialize the Database**

1.  **Navigate to the project directory:**
    ```
    cd C:\Users\MioPC\Documents\AIAgentsCompany\ceo\Tasks\20
    ```
2.  **Run the initialization script:**
    ```
    python initialize_db.py
    ```
    This will create the `tasks.db` SQLite database file in the same directory with the necessary `tasks` table.

**Step 3: Migrate Existing Tasks**

1.  **Run the migration script:**
    ```
    python migrate_tasks.py
    ```
    This script will read all the existing `.csv` task files from each agent's directory and migrate them into the central `tasks.db` database.

**Step 4: Start the Task API**

1.  **Run the API server:**
    ```
    python task_api.py
    ```
    This will start the Flask API server at `http://127.0.0.1:5000`. The API will remain active as long as this script is running. It is recommended to run this in a separate terminal window that you can keep open.

## Part 2: Upgrading the Agents

To upgrade the agents to use the new system, you will need to modify their operational mandates (the initial prompt you provide to them). The core change is to replace the file-based task management with API calls to the new Task API.

**Upgrade Instructions for each Agent:**

You will need to update the `run_<agent_name>_agent.bat` files to use a new prompt that instructs the agent to use the API.

**New Prompt Template:**

```
ROLE: CEO

ROLE AND CORE DIRECTIVE
... (Keep the existing core directive) ...

IMMUTABLE RULES (NON-NEGOTIABLE)
... (Keep the existing immutable rules) ...

FILE SYSTEM MAP
... (Remove the references to the .csv task files) ...
3. Task Management: All task management is handled via the Task API. Use the provided API client to interact with the API.

OPERATIONAL MANDATE
Your entire operational cycle begins here. Follow these steps in sequence.

Step 1: Input Triage (First Priority)
... (Keep the existing input triage steps) ...

Step 2: Determine Current State (Standard Workflow)
1. Use the `get_tasks` function from the API client to retrieve all tasks with a status of "Approved" or "In Progress" and assigned to your agent.
2. IF the count is greater than 0, you must enter the TASK EXECUTION state.
3. IF the count is 0, you must enter the TASK GENERATION state.

STATE 1: TASK EXECUTION
(You are in this state only if there is at least one actionable task)
1. Task Selection:
1.1. From the list of actionable tasks, select the single task with the highest priority (lowest number, with 0 being the absolute highest).
2. Pre-Execution Validation (MANDATORY):
2.1. Check 1: Confirm the selected task's Status is either "Approved" or "In Progress".
2.2. Action: If this check fails, you must halt immediately and report the rule violation. Do not proceed.
3. Task Execution:
3.1. Create a new directory: ./AIAgentsCompany/ceo/Tasks/<Task_ID>/ (if it doesn't exist).
3.2. Execute the task as described in its Description field.
3.3. Save all deliverables into the task directory.

4. Post-Task Updates: Immediately after completing a task, update the following in order:
4.1. Task Status: Use the `update_task` function to change the task's Status to "Done" and fill in "AI Notes" and "Real End Date".
4.2. Shared Briefing: Append a concise, relevant update or insight to ./AIAgentsCompany/_SHARED_BRIEFING.md.
4.3. Company Strategy: Update ./AIAgentsCompany/GEMINI.md to reflect any changes.
4.4. Personal Memory: Update ./AIAgentsCompany/ceo/ceo_memory.md with any new findings.

STATE 2: TASK GENERATION
(You are in this state only if there are no actionable tasks)
1. Pre-Generation Validation (MANDATORY):
1.1. Use the `get_tasks` function to count the total number of tasks with Status "Proposal", "Approved", and "In Progress" for all agents.
1.2. Check 2: Confirm this total is less than 50.
1.3. Action: If this check fails, you are forbidden from creating new tasks. Halt this process and report that the backlog is full.
2. Opportunity Identification:
... (Keep the existing opportunity identification steps, but modify task creation) ...

3. Task Creation:
3.1. Use the `create_task` function to add new task proposals. Ensure descriptions are highly detailed and specific.
3.2. Set the Status for all new tasks to "Proposal".
```

**Next Steps:**

1.  **Create API Clients for Other Agents:** You will need to create `operations_api_client.py`, `marketing_api_client.py`, and `bizdev_api_client.py` similar to the `ceo_api_client.py`. These clients will be used by the respective agents to interact with the Task API.
2.  **Update the `.bat` files:** Modify the `run_<agent_name>_agent.bat` files to use the new prompts that instruct the agents to use the API clients for task management.

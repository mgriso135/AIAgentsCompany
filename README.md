# Gemini CLI Agents

This repository contains a setup for running two specialized Gemini CLI agents: a Developer Agent and a Marketing Agent. These agents are designed to work collaboratively, with the Marketing Agent briefing the Developer Agent on tasks via a shared briefing file.

## Prerequisites

To run these agents, you need to have the Gemini CLI installed and configured on your system.

*   **Gemini CLI**: Please refer to the official Gemini CLI documentation for installation instructions.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd AIAgentsCompany
    ```

2.  **Ensure Agent Files are Present**: Verify that the `gemini_agents` directory and its contents are present in your project root:
    ```
    AIAgentsCompany/
    ├───GEMINI.md
    ├───launch_dev_agent.ps1
    ├───launch_mktg_agent.ps1
    ├───README.md
    ├───run_dev_agent.bat
    ├───run_mktg_agent.bat
    ├───.git/...
    └───gemini_agents/
        ├───_SHARED_BRIEFING.md
        ├───developer/
        │   ├───developer_memory.md
        │   ├───developer_tasks.csv
        │   └───Tasks/
        └───marketing/
            ├───marketing_memory.md
            ├───marketing_tasks.csv
            └───Tasks/
    ```

## Agent Workflows

### 1. Marketing Agent

The Marketing Agent is responsible for generating marketing-related content and tasks. It can also brief the Developer Agent on new development tasks.

*   **Purpose**: To handle marketing initiatives, content creation, and to communicate development needs to the Developer Agent.
*   **Task Management**: The Marketing Agent manages its individual tasks using `gemini_agents/marketing/marketing_tasks.csv`.
*   **Launch**:
    *   **Windows (PowerShell)**:
        ```powershell
        ./launch_mktg_agent.ps1
        ```
    *   **Windows (Command Prompt)**:
        ```bash
        run_mktg_agent.bat
        ```

### 2. Developer Agent

The Developer Agent is designed to handle software development tasks. It receives its instructions and tasks from the Marketing Agent via the shared briefing file.

*   **Purpose**: To implement features, fix bugs, and perform other development-related tasks based on the briefs from the Marketing Agent.
*   **Task Management**: The Developer Agent manages its individual tasks using `gemini_agents/developer/developer_tasks.csv`.
*   **Launch**:
    *   **Windows (PowerShell)**:
        ```powershell
        ./launch_dev_agent.ps1
        ```
    *   **Windows (Command Prompt)**:
        ```bash
        run_dev_agent.bat
        ```

### Inter-Agent Communication

The two agents communicate primarily through the `gemini_agents/_SHARED_BRIEFING.md` file, which serves as a shared briefing space.

*   The **Marketing Agent** writes development tasks and briefs into `_SHARED_BRIEFING.md`.
*   The **Developer Agent** reads from `_SHARED_BRIEFING.md` to understand its tasks and context.

This shared file acts as a central point for task hand-off and information exchange between the agents. While `_SHARED_BRIEFING.md` facilitates communication, each agent maintains its own task list (`*.csv` files) for managing their individual work.

## Usage Guide

Follow these steps to use the agents effectively:

1.  **Start the Marketing Agent**:
    Launch the Marketing Agent using one of the methods described above.

2.  **Brief the Marketing Agent**:
    Interact with the Marketing Agent and provide it with marketing tasks or instruct it to create a development brief for the Developer Agent. For example, you might ask the Marketing Agent to "Write a brief for the developer agent to create a new user authentication module."

3.  **Marketing Agent Creates Brief**:
    The Marketing Agent will process your request and, if it involves development, will write the brief into `gemini_agents/_SHARED_BRIEFING.md`.

4.  **Start the Developer Agent**:
    Once the Marketing Agent has created a brief, launch the Developer Agent.

5.  **Developer Agent Reads Brief**:
    The Developer Agent will automatically read the contents of `gemini_agents/_SHARED_BRIEFING.md` to understand its new task.

6.  **Developer Agent Executes Task**:
    The Developer Agent will then proceed to work on the development task as outlined in the shared briefing.

7.  **Monitor and Iterate**:
    You can monitor the progress of both agents. If further clarification or new tasks are needed, you can interact with the respective agent. The `_SHARED_BRIEFING.md` can be updated by the Marketing Agent for subsequent development tasks.

This setup allows for a structured workflow where marketing requirements are translated into actionable development tasks through automated agent interaction.

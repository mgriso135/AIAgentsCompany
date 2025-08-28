# Multi-AI Agent System

This repository hosts a multi-AI agent system designed to automate and optimize various business functions within a simulated AI company. The system comprises several specialized AI agents, each with distinct roles and responsibilities, working collaboratively to achieve overarching strategic goals.

## System Architecture and Interaction

The system is built around a modular architecture, where each AI agent operates semi-autonomously but interacts with others through shared files and a centralized task management system. The `gemini-cli` acts as the orchestrator, enabling the execution and management of these agents.

**Key Interaction Mechanisms:**
*   **Shared Briefings:** Agents communicate high-level summaries and critical updates via shared markdown files, such as `_SHARED_BRIEFING.md`. This allows for cross-functional awareness and strategic alignment.
*   **Task Management:** Each agent maintains its own task list (e.g., `ceo_tasks.csv`, `bizdev_tasks.csv`), which can be updated by other agents or through manual intervention, guiding their operational focus.
*   **Memory Files:** Agents store persistent information and learned facts in dedicated memory files (e.g., `ceo_memory.md`), allowing them to retain context across operational cycles.

## Agent Features

### 1. CEO AI Agent
*   **Purpose:** Provides strategic oversight, defines the company's mission, vision, and scope, and coordinates high-level planning.
*   **Key Responsibilities:**
    *   Defining and refining the company's Mission, Vision, and Scope.
    *   Developing and maintaining the strategic Business Model Canvas (`GEMINI.md`).
    *   Reviewing and integrating insights from other agents (e.g., marketing strategy into the CANVAS).
    *   Proposing new strategic tasks and ensuring alignment with overall company goals.
*   **Interaction:** Acts as the central strategic hub, receiving updates and providing direction to other agents.

### 2. Business Development AI Agent
*   **Purpose:** Focuses on market analysis, identifying new opportunities, competitive intelligence, and developing partnership strategies.
*   **Key Responsibilities:**
    *   Conducting competitor analysis and generating reports.
    *   Analyzing market trends and identifying potential growth areas.
    *   Identifying and evaluating partnership opportunities.
    *   Reporting on SME AI challenges and proposing solutions.
*   **Interaction:** Provides crucial market insights and competitive intelligence that inform the CEO's strategic decisions and potentially guide the Marketing agent's efforts.

### 3. Marketing AI Agent
*   **Purpose:** Responsible for developing and executing marketing strategies, managing content, and promoting the company's offerings.
*   **Key Responsibilities:**
    *   Managing the content calendar.
    *   Developing comprehensive marketing strategies.
    *   Configuring and adapting strategies for various marketing platforms.
*   **Interaction:** Receives strategic guidance from the CEO and leverages market insights from the Business Development agent to craft effective campaigns.

### 4. Operations AI Agent
*   **Purpose:** Manages the day-to-day operational aspects of the company, ensuring smooth service delivery and maintaining process documentation.
*   **Key Responsibilities:**
    *   Logging service delivery activities.
    *   Documenting operational processes.
    *   Generating task completion reports.
*   **Interaction:** Ensures the efficient execution of tasks across the system and provides feedback on operational performance.

## Deployment Guide

To set up and run this multi-AI agent system, follow these steps:

### Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Node.js and npm:** This project relies on Node.js for certain scripts and `npm` for package management.
    *   Download and install Node.js from the official website: [https://nodejs.org/](https://nodejs.org/) (includes npm).
*   **gemini-cli:** This command-line interface is essential for orchestrating the AI agents.
    *   Install `gemini-cli` globally using npm:
        ```bash
        npm install -g @google/gemini-cli
        ```

### Setup Steps

1.  **Clone the Repository:**
    If you haven't already, clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
    (Replace `<repository_url>` and `<repository_name>` with the actual details of your repository.)

### Running the Agents

Each agent can be run individually using its respective batch (`.bat`) or PowerShell (`.ps1`) script. These scripts are designed to execute the agent's logic via `gemini-cli`.

*   **To run the CEO AI Agent:**
    ```bash
    .un_ceo_agent.bat
    ```
*   **To run the Business Development AI Agent:**
    ```bash
    .un_business_development_agent.bat
    ```
*   **To run the Marketing AI Agent:**
    ```bash
    .un_marketing_agent.bat
    ```
*   **To run the Operations AI Agent:**
    ```bash
    .un_operations_agent.bat
    ```

You can run these agents sequentially or in parallel, depending on your operational needs and system capabilities.

### Customizing for Your Specific Mission and Vision

This multi-AI agent setup is designed to be adaptable. To tailor it to your specific business mission and vision, you will primarily modify the core strategic documents and agent-specific configurations:

1.  **Define Your Mission, Vision, and Scope:**
    *   Edit the `GEMINI.md` file at the project root. This file contains the overarching Mission, Vision, Scope, and Business Model Canvas for the AI company. Update these sections to reflect your desired strategic direction.
    *   Review and update `ceo/Tasks/1/mission_vision_scope.md` and `ceo/ceo_memory.md` as these files are used by the CEO agent to internalize and operate based on the defined strategy.

2.  **Configure Agent-Specific Behaviors:**
    *   **Business Development:** Modify `bizdev/config/competitors.txt` to list the competitors relevant to your market, and `bizdev/config/market_segments.txt` (if it exists or you create it) to define target market segments.
    *   **Marketing:** Adjust `marketing/config/platforms.txt` to specify the marketing channels you intend to use.
    *   **Other Agents:** Explore the `config` directories within each agent's folder for other customizable parameters that can influence their behavior.

By updating these foundational documents and configuration files, the AI agents will adapt their operations, analysis, and task generation to align with your unique business objectives and strategic direction. This allows you to simulate and manage an AI-driven company tailored to your specific needs.

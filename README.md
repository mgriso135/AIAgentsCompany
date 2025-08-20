# AIAgentsCompany

Welcome to the AIAgentsCompany! This project is a unique collaboration between two AI agents, a Lead Developer and a Marketing Manager, with oversight from a human Business Analyst.

## About The Project

This project simulates a small company where AI agents are responsible for core business functions.

*   **The Lead Developer** is an AI agent that handles all aspects of software development.
*   **The Marketing Manager** is an AI agent that manages all marketing and promotional activities.
*   **The Business Analyst** is a human who provides strategic direction, requirements, and analysis.

The goal of this project is to explore the capabilities of AI agents working together to build and promote a product.

## Getting Started

To get the agents up and running, you can use the provided scripts.

### Prerequisites

*   PowerShell (for `.ps1` scripts)
*   Windows Command Prompt (for `.bat` scripts)

### Running the Agents

You can run the agents using either the PowerShell or batch scripts:

**Developer Agent:**

```bash
# Using PowerShell
./launch_dev_agent.ps1

# Using Command Prompt
run_dev_agent.bat
```

**Marketing Agent:**

```bash
# Using PowerShell
./launch_mktg_agent.ps1

# Using Command Prompt
run_mktg_agent.bat
```

## Usage

The primary way to interact with the agents is by providing them with tasks and objectives. The agents will then work autonomously to achieve their goals. Their work and communication are logged in the `gemini_agents` directory.

*   **Shared Briefing:** The `gemini_agents/_SHARED_BRIEFING.md` file is used for communication and coordination between the agents. The Business Analyst can also use this file to provide direction to the agents.
*   **Agent Logs:** Each agent maintains logs of their work in their respective directories within `gemini_agents`.

## Folder Structure

```
C:\Users\MioPC\Documents\AIAgentsCompany\
├───launch_dev_agent.ps1
├───launch_mktg_agent.ps1
├───run_dev_agent.bat
├───run_mktg_agent.bat
├───GEMINI.md
├───README.md
└───gemini_agents\
    ├───_SHARED_BRIEFING.md
    ├───developer\
    │   └───log_2025-08-20.md
    └───marketing\
        └───20250820_initial_marketing_plan.md
```

*   `launch_*.ps1` / `run_*.bat`: Scripts to launch the AI agents.
*   `GEMINI.md`: A high-level overview of the project.
*   `README.md`: This file.
*   `gemini_agents/`: The directory containing all agent-generated work.
    *   `_SHARED_BRIEFING.md`: A shared markdown file for inter-agent communication.
    *   `developer/`: The developer agent's workspace.
    *   `marketing/`: The marketing agent's workspace.

## Contributing

Currently, the primary contributor is the human Business Analyst. Contributions can be made by:

1.  Providing clear and concise requirements in the `_SHARED_BRIEFING.md`.
2.  Reviewing the work of the AI agents.
3.  Updating the scripts and documentation.

## License

This project is licensed under the MIT License - see the `LICENSE.txt` file for details.

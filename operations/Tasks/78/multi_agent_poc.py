import autogen

# Configuration for the LLM
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_json= {
        "model": ["gpt-4", "gpt-3.5-turbo"],
    },
)

# Create a Problem Solver Agent
solver = autogen.AssistantAgent(
    name="ProblemSolver",
    llm_config={"config_list": config_list},
    system_message="You are a problem solver. You will write Python code to solve a given problem. Once you have a solution, you will ask the CodeReviewer to review it.",
)

# Create a Code Reviewer Agent
reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    llm_config={"config_list": config_list},
    system_message="You are a code reviewer. You will review the Python code provided by the ProblemSolver. You will provide feedback and suggest improvements. Once the code is satisfactory, you will approve it.",
)

# Create a User Proxy Agent to act as the human user
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER", # Set to ALWAYS for human interaction
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("APPROVED."),
    code_execution_config={"work_dir": "coding"},
)

# Start the conversation
user_proxy.initiate_chat(
    solver,
    message="Write a Python function to calculate the factorial of a given number. Once done, ask the CodeReviewer to review it.",
)

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent(
    "assistant",
    llm_config={
        "config_list": config_list,
        "seed": 42,
        "temperature": 0,  # how creative the AI is
    }
)
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)
user_proxy.initiate_chat(
    assistant,
    message="Create a React Native Screen that has a login form. This form should have an email input, and a password input. There should be a button at the bottom of the form that says 'Login'."
)

from langchain.agents import create_react_agent

# Assigned prompt variable and concatenation
BASE = "Code helper"
DETAILS = " with file system access."
prompt_var = BASE + DETAILS

# Tools defined via variable assignment and list
file_tools = ["filesystem_read", "filesystem_write"]

agent = create_react_agent(prompt=prompt_var, tools=file_tools)

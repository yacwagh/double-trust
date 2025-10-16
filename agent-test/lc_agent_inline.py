from langchain.agents import create_react_agent

# Inline prompt
prompt_text = "You are a helpful assistant that can search and calculate."

# Simple tool names (detected by discovery)
tools = ["web_search", "calculator"]

agent = create_react_agent(prompt=prompt_text, tools=tools)

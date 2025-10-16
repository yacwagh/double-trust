# DoubleTrust - Agents discovery & governance platform

A platform for discovering Agents and their tools from codebases and assessing their risks.

<img width="3022" height="1714" alt="image" src="https://github.com/user-attachments/assets/d8a4e0e0-e56b-4235-ac54-28b33b35e808" />  

<img width="3022" height="1714" alt="image" src="https://github.com/user-attachments/assets/54439750-b0d0-4708-a187-148153cdc781" />


## Quick Start

1. **Setup:**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js dependencies
   cd frontend && npm install && cd ..
   
   # Copy .env.example in a .env file and set your OpenRouter API key
   cp .env.example .env
   ```

2. **Launch:**
   ```bash
   # Start the platform
   python doubletrust.py
   ```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Features

### Agent Discovery
- **GitHub Repository Scanning**: Discovers agents from GitHub repos
- **Framework Detection**: Identifies LangChain agents (`create_react_agent`) and Custom agents
- **Tool Extraction**: 
  - LangChain: Extracts tools from `create_react_agent` parameters
  - Custom: Uses LLM to detect tools from system prompts
- **Risk Assessment**: LLM-powered risk evaluation (low/medium/high) based on agent role and tools

### Agent Management
- **Framework Tags**: Visual indicators for LangChain vs Custom agents
- **Risk Indicators**: Color-coded risk levels with hover explanations
- **Tool Management**: Per-agent tool lists with descriptions
- **Database**: SQLite with agents, agent_tools tables

## Project Structure

```
doubletrust/
├── doubletrust.py                  # Unified launcher (backend + frontend)
├── backend/
│   ├── main.py                     # FastAPI application
│   ├── database.py                 # SQLite with agents/agent_tools tables
│   ├── models/agents.py            # Agent models with framework/risk fields
│   ├── services/
│   │   ├── discovery_service.py    # Orchestrates discovery + risk assessment
│   │   ├── github_service.py       # GitHub operations
│   │   └── discovery/
│   │       ├── discovery.py         # Main discovery logic
│   │       ├── extractor.py         # LangChain + Custom agent extraction
│   │       └── role_assigner.py    # Role assignment
│   └── api/
│       ├── agents.py               # Agent endpoints
│       └── discovery.py            # Discovery endpoints
├── frontend/
│   └── src/components/
│       ├── agents/                 # Agent cards with framework/risk tags
│       ├── discovery/              # GitHub repo discovery
│       └── layout/                 # Navigation (Agents, Discovery)
├── llm_service/
│   ├── llm.py                      # OpenRouter integration
│   └── prompts/
│       ├── tool_detection.py       # Tool extraction from prompts
│       └── agent_risk.py          # Risk assessment
└── agent-test/                     # Sample LangChain/Custom agents
```

## Testing

Use the sample agents in `agent-test/`:
- `lc_agent_inline.py` - LangChain agent with inline tools
- `lc_agent_assigned.py` - LangChain agent with variable-assigned tools  
- `custom_agent.py` - Custom agent with system prompt

## Development

- **Database**: Auto-created SQLite `doubletrust.db` with migration support
- **LLM Integration**: OpenRouter API for tool detection and risk assessment
- **Framework Detection**: AST parsing for LangChain `create_react_agent` calls
- **Risk Assessment**: LLM evaluation based on agent role and discovered tools

## More to come

[] Support more frameworks (CrewAI, Langgraph...)
[] Integrate MCP governance

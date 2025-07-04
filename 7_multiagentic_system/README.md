# Multi-Agent System with LangGraph

This project implements a multi-agent system using LangGraph that coordinates specialized agents to solve different types of problems. The system consists of a math expert agent and a research expert agent, orchestrated by a supervisor agent.

## Architecture

The system consists of:

1. **Research Expert**: Capable of searching the web using DuckDuckGo for information gathering and current events.
2. **Math Expert**: Specialized in mathematical operations (addition, multiplication).
3. **Supervisor**: Coordinates between agents based on the task requirements.


Run the application with:

```
python 7_multiagentic_system/app.py
```

The system will process the example query "what is quantum computing?" and route it to the appropriate agent (research expert in this case).

## Components

### Agents (`agents.py`)

Defines specialized agents using the LangGraph framework:
- `math_agent`: Handles mathematical operations
- `research_agent`: Performs web searches with DuckDuckGo

### Tools (`tools.py`)

Provides utility functions:
- Web search via DuckDuckGo
- Basic math operations (add, multiply, subtract, divide)

### Application (`app.py`)

The main application that:
- Creates the supervisor workflow
- Compiles the agent graph
- Visualizes the workflow
- Handles user queries

## Visualization

The system generates a workflow graph visualization saved as `workflow_graph.png` to help understand the agent routing logic.

## Example

When you run the application, it processes a default query about quantum computing, routing it to the research expert agent which uses DuckDuckGo to search for relevant information.

You can modify the query in `app.py` to test different scenarios:
- For math problems: "what is 25 multiplied by 16?"
- For research questions: "what are the latest developments in AI?"

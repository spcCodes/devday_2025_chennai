# Augmented LLM System

A tool-enhanced conversational AI agent built with LangGraph.

## Overview

This project demonstrates how to build an AI agent that can:
- Process natural language queries
- Utilize various tools to augment its capabilities
- Maintain context through state management
- Provide curated, coherent responses

## Architecture

The system is structured around four main components:

### Models (`models.py`)
- `AppState`: Tracks conversation messages and processing flow
- `FinalResponse`: Formats clean outputs for end users

### Tools (`tools.py`)
- Web search via Tavily Search API
- Date retrieval
- Calculator functions (add, subtract, multiply, divide)

### Processing Nodes (`nodes.py`)
- `agent_node`: Uses GPT-4o-mini to process inputs and determine actions
- `tool_wrapper`: Executes tools when needed
- `response_curator`: Synthesizes information from the conversation
- `output_formatter`: Formats the final response

### Application Flow (`app.py`)
- Orchestrates the workflow using LangGraph's `StateGraph`
- Creates a directed graph with conditional routing
- Handles input/output transformation

## Workflow

1. User query enters the system → processed by agent node
2. Agent determines if tools are needed
   - If yes → routes to tool_wrapper → back to agent
   - If no → routes to curator
3. Curator synthesizes information into coherent answer
4. Output formatter prepares final response

## Example Usage

```python
# Initialize with a question
initial_state = AppState(
    messages=[HumanMessage(content="What is the weather in Tokyo and can you add 15 to the temperature and then multiply by 10")],
    node_trace=[]
)

# Run the workflow
result = app.invoke(initial_state)

# Get the final response
final_response = result.get("final_response")
print(final_response.response)
```

## Setup

1. Install dependencies:
   ```
   pip install langchain langchain-openai langgraph pydantic python-dotenv
   ```

2. Configure environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

3. Run the application:
   ```
   python augmented_llm/app.py
   ```


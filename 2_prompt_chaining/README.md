# Prompt Chaining with LangGraph

This project demonstrates a simple prompt chaining workflow using LangGraph to create a joke generation pipeline. The application takes a user-provided topic and passes it through a series of LLM calls, with each step refining the joke until a final polished version is produced.

## Architecture

The project uses a directed graph workflow with:
- **State Management**: TypedDict for tracking joke evolution
- **LLM Integration**: OpenAI's GPT-4o-mini model via LangChain
- **Workflow Orchestration**: LangGraph for managing the multi-step process

## Workflow Steps

1. **Generate Initial Joke**: Creates a basic joke about the requested topic
2. **Quality Check**: Conditionally routes based on whether the joke has proper structure
3. **Improve Joke**: Enhances the joke by adding wordplay
4. **Polish Joke**: Adds a surprising twist for the final version

## Components

### Models (`models.py`)
Defines the `State` TypedDict that tracks the joke's progression through:
- `topic`: User's requested subject
- `joke`: Initial generated joke
- `improved_joke`: Enhanced version with wordplay
- `final_joke`: Polished joke with a twist

### Nodes (`nodes.py`)
Contains the processing functions:
- `generate_joke`: First LLM call to create initial joke
- `check_punchline`: Conditional router checking for "?" or "!" in joke
- `improve_joke`: Second LLM call to add wordplay
- `polish_joke`: Third LLM call to add surprise twist

### App (`app.py`)
Orchestrates the workflow by:
- Defining the directed graph structure
- Adding nodes and conditional paths
- Compiling the workflow
- Visualizing the graph (saved as workflow_graph.png)

## Usage

```python
from prompt_chaining.app import app

# Generate a joke about AI
result = app.invoke({"topic": "AI"})
print("Final Joke:", result["final_joke"])
```


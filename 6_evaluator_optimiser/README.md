# Joke Evaluator and Optimizer

This project uses LangGraph to create a workflow that generates jokes based on a given topic, evaluates them, and improves them through feedback until they are deemed funny.

## Overview

The system consists of three main components:
- **Generator**: Creates jokes about a specified topic
- **Evaluator**: Determines if a joke is funny or not with feedback
- **Optimizer**: Routes jokes back to the generator for improvement if they're not funny

## Architecture

The project uses LangGraph to create a directed graph workflow:
1. The joke generator creates an initial joke based on a topic
2. The evaluator determines if the joke is funny or not
3. If the joke is funny, the workflow ends
4. If the joke is not funny, feedback is provided to the generator to create an improved joke

## Components

### Models (models.py)
- `Feedback`: Pydantic model for structured evaluation output with grade and feedback
- `State`: TypedDict that tracks the state of the workflow (joke, topic, feedback, and evaluation)

### Nodes (nodes.py)
- `llm_call_generator`: Generates jokes using LLM, incorporating feedback if available
- `llm_call_evaluator`: Evaluates jokes using structured output
- `route_joke`: Routes the workflow based on the evaluation result

### Main Application (app.py)
- Builds and compiles the workflow using LangGraph
- Visualizes the workflow as a Mermaid diagram
- Provides an entrypoint to invoke the workflow with a topic

## Usage

```python
# Import the workflow
from app import optimizer_workflow

# Run the joke optimizer with a topic
result = optimizer_workflow.invoke({"topic": "Cats"})

# Get the optimized joke
print(result["joke"])
```


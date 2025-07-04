# LangGraph Routing Example

This example demonstrates how to implement conditional routing in LangGraph, creating a flexible content generation workflow.

## Overview

This application uses LangGraph to route user input to different content generation nodes based on the user's request. The workflow:

1. Takes a user input
2. Routes it to one of three content generators (story, joke, or poem)
3. Returns the generated content

## Project Structure

- `app.py`: Defines the LangGraph workflow and connects nodes
- `nodes.py`: Contains node functions for routing and content generation
- `models.py`: Defines data structures for state management and routing

## How It Works

### State Management

The application uses a TypedDict to manage state:

```python
class State(TypedDict):
    input: str      # User's input request
    decision: str   # Routing decision (story/joke/poem)
    output: str     # Generated content
```

### Routing Logic

The routing mechanism uses a structured output approach with a Pydantic model:

```python
class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        default="story", description="The next step in the routing process"
    )
```

The `route_decision` node analyzes the user's input and determines which content type to generate:

```python
def route_decision(state: State):
    result = router.invoke([
        SystemMessage(content="Route the input to story, joke, or poem based on the user's request."),
        HumanMessage(content=state["input"]),
    ])
    return {"decision": result.step}
```

### Content Generation Nodes

Three specialized nodes handle content generation:

1. `write_story`: Generates a narrative based on the input
2. `write_joke`: Creates humor related to the input
3. `write_poem`: Composes poetry inspired by the input

### Workflow Graph

The workflow is structured as follows:

```
START → route_decision → [write_story | write_joke | write_poem] → END
```

The conditional routing is implemented with:

```python
workflow.add_conditional_edges(
    "route_decision",
    get_next_node,
    {
        "write_story": "write_story",
        "write_joke": "write_joke",
        "write_poem": "write_poem",
    },
)
```

## Running the Example

Execute the application:

```bash
python app.py
```

For a sample input like "I want to hear a story", the system will:
1. Route to the `write_story` node
2. Generate a story
3. Output the result

## Visualizing the Workflow

The application includes a function to visualize the workflow as a PNG:

```python
display_graph(app)
```

This creates a `workflow_graph.png` file in the current directory.

## Key Concepts Demonstrated

- Conditional routing in LangGraph
- Structured output for decision making
- Dynamic LLM-based routing
- State management across nodes
- Workflow visualization

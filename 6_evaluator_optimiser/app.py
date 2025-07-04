import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

#custom imports
from models import State
from nodes import llm_call_generator, llm_call_evaluator, route_joke

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        # Use simpler approach without specific MermaidDrawMethod
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("6_evaluator_optimiser/workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        print(e)

# Build workflow
optimizer_builder = StateGraph(State)

# Add the nodes
optimizer_builder.add_node("llm_call_generator", llm_call_generator)
optimizer_builder.add_node("llm_call_evaluator", llm_call_evaluator)

# Add edges to connect nodes
optimizer_builder.add_edge(START, "llm_call_generator")
optimizer_builder.add_edge("llm_call_generator", "llm_call_evaluator")
optimizer_builder.add_conditional_edges(
    "llm_call_evaluator",
    route_joke,
    {  # Name returned by route_joke : Name of next node to visit
        "Accepted": END,
        "Rejected + Feedback": "llm_call_generator",
    },
)

# Compile the workflow
optimizer_workflow = optimizer_builder.compile()

# Show the workflow
display_graph(optimizer_workflow)

if __name__ == "__main__":
    #invoke app
    state = optimizer_workflow.invoke({"topic": "Cats"})
    print(state["joke"])

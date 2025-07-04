import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

#custom imports
from models import State, WorkerState
from nodes import orchestrator, llm_call, synthesizer, assign_workers

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        # Use simpler approach without specific MermaidDrawMethod
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("5_orchestrator_worker/workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        print(e)


    
# Build workflow
orchestrator_worker_builder = StateGraph(State)

# Add the nodes
orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("llm_call", llm_call)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)

# Add edges to connect nodes
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator", assign_workers, ["llm_call"]
)
orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile the workflow
orchestrator_worker = orchestrator_worker_builder.compile()

# Show the workflow
# display_graph(orchestrator_worker)

if __name__ == "__main__":
    #invoke app
    result = orchestrator_worker.invoke({"topic": "Create a report on LLM scaling laws"})
    print(result["final_report"])
    from IPython.display import Markdown

    Markdown(result["final_report"])


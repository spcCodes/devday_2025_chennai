import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

#custom imports
from models import State
from nodes import generate_joke, improve_joke, polish_joke, check_punchline

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("prompt_chaining/workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        # This requires some extra dependencies and is optional
        print(e)

#build workflow
workflow  = StateGraph(State)

#add nodes
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

#add edges
workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke", 
    check_punchline, 
    {"Pass": "improve_joke", "Fail": END}
)
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

app = workflow.compile()

display_graph(app)

if __name__ == "__main__":
    result = app.invoke({"topic": "tell a joke about AI"})
    print("Joke: ", result["final_joke"])

    print(result)
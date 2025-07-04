import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

#custom imports
from models import State
from nodes import write_story, write_joke, write_poem, route_decision, get_next_node

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        # Use simpler approach without specific MermaidDrawMethod
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("4_routing/workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        print(e)


#build workflow
workflow = StateGraph(State)

#add nodes

workflow.add_node("write_story", write_story)
workflow.add_node("write_joke", write_joke)
workflow.add_node("write_poem", write_poem)
workflow.add_node("route_decision", route_decision)

#add edges
workflow.add_edge(START, "route_decision")
workflow.add_conditional_edges(
    "route_decision",
    get_next_node,
    {
        "write_story": "write_story",
        "write_joke": "write_joke",
        "write_poem": "write_poem",
    },
)
workflow.add_edge("write_story", END)
workflow.add_edge("write_joke", END)
workflow.add_edge("write_poem", END)

#compile app
app = workflow.compile()



if __name__ == "__main__":
    #invoke app
    result = app.invoke({"input": "I want to hear a story"})
    print(result["output"])
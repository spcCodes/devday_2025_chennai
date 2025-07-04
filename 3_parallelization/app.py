import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

#custom imports
from models import State
from nodes import generate_joke, generate_story, generate_poem, combine_outputs

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        # Use simpler approach without specific MermaidDrawMethod
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("3_parallelization/workflow_graph.png", "wb") as f:
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
workflow.add_node("generate_story", generate_story)
workflow.add_node("generate_poem", generate_poem)
workflow.add_node("combine_outputs", combine_outputs)

#add edges
workflow.add_edge(START, "generate_joke")
workflow.add_edge(START, "generate_story")
workflow.add_edge(START, "generate_poem")
workflow.add_edge("generate_joke", "combine_outputs")
workflow.add_edge("generate_story", "combine_outputs")
workflow.add_edge("generate_poem", "combine_outputs")
workflow.add_edge("combine_outputs", END)

#compile app
app = workflow.compile()

#display graph
display_graph(app)

if __name__ == "__main__":
    #invoke app
    result = app.invoke({"topic": "cats"})
    print(result["combined_output"])



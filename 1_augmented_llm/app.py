import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from langchain_core.messages import HumanMessage
from IPython.display import Image, display

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        # This requires some extra dependencies and is optional
        print(e)

# Import our custom components
from models import AppState, FinalResponse
from nodes import agent_node, tool_wrapper, response_curator, output_formatter

# Define the graph
workflow = StateGraph(AppState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_wrapper)
workflow.add_node("curator", response_curator)
workflow.add_node("output_formatter", output_formatter)

# Set entry point
workflow.set_entry_point("agent")

# Add conditional edges using the prebuilt tools_condition
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "curator"  # Send to curator instead of ending
    }
)

# Add an edge from tools back to agent
workflow.add_edge("tools", "agent")

# Add an edge from curator to output formatter and from output formatter to END
workflow.add_edge("curator", "output_formatter")
workflow.add_edge("output_formatter", END)

# Compile the workflow
app = workflow.compile()

if __name__ == "__main__":
    # Initialize with a question using proper message format
    initial_state = AppState(
        messages=[HumanMessage(content="What is the weather in Bnagalore and can you add 15 to the temperature and then multiply by 10")],
        node_trace=[]
    )
    
    # Run the workflow
    result = app.invoke(initial_state)
    
    # Display the graph
    display_graph(app)

    # Print just the final response content
    print("\nFinal Response:")
    
    # Access the FinalResponse object from the result
    final_response = result.get("final_response")
    if final_response:
        print(final_response.response)
        #You could also access other metadata if needed
        print(f"Node trace: {final_response.metadata.get('node_trace')}")
    else:
        # Fallback to original method
        response_message = result.get("messages", [])
        if response_message:
            print(response_message[-1].content)
        else:
            print("No response found in result")






import os
from dotenv import load_dotenv
load_dotenv()
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from langchain_openai import ChatOpenAI
#custom imports 
from agents import research_agent, math_agent

from langgraph_supervisor import create_supervisor

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def display_graph(app):
    # this function will display the graph of the app and save it
    try:
        # Use simpler approach without specific MermaidDrawMethod
        graph_png = app.get_graph().draw_mermaid_png()
        # Save the graph as PNG
        with open("7_multiagentic_system/workflow_graph.png", "wb") as f:
            f.write(graph_png)
        # Display the graph
        display(Image(graph_png))
    except Exception as e:
        print(e)

        
# Create supervisor workflow
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
        "If a query involves both research and math, first use research_agent to get data, "
        "then use math_agent with the research results. "
        "IMPORTANT: Each agent should be called at most once for a specific subtask."
    )
)
# Compile and run
app = workflow.compile()

if __name__ == "__main__":
    # Use a simpler query for testing
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": "what is temp of delhi now and can you add 15 to the temperature and then multiply by 10"  # Simple math query for testing
            }
        ]
    })
    print(result)
    # Extract and print only the content of the last message
    if result and "messages" in result and result["messages"]:
        last_message = result["messages"][-1]
        print("\nFinal Response:")
        print(last_message.content)
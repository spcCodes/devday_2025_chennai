from typing import Dict, Any
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from tools import search_web, get_current_date, add_numbers, subtract_numbers, multiply_numbers, divide_numbers

# Import our state definitions
from models import AppState, FinalResponse

# Initialize tools and models
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search_web, get_current_date, add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
model_with_tools = model.bind_tools(tools)

# Create tool node
base_tool_node = ToolNode(tools=tools)

def agent_node(state: AppState) -> AppState:
    """LLM agent that can use tools."""
    response = model_with_tools.invoke(state.messages)
    
    # Add node trace to track flow
    updated_trace = state.node_trace + ["agent"]
    
    return AppState(messages=[response], node_trace=updated_trace)


def tool_wrapper(state: AppState) -> AppState:
    """Wrap the tool node to maintain our state structure."""
    # The tool node expects a dict with "messages"
    tool_input = {"messages": state.messages}
    
    # ToolNode's invoke method must be used, not calling the object directly
    tool_output = base_tool_node.invoke(tool_input)
    
    # Add node trace to track flow
    updated_trace = state.node_trace + ["tool"]
    
    return AppState(messages=tool_output["messages"], node_trace=updated_trace)


def response_curator(state: AppState) -> AppState:
    """Curate a final response based on all conversation history."""
    # We'll use a system prompt to instruct the model to synthesize information
    curator_prompt = """You are a response curator. Review the entire conversation history and tool outputs.
    Synthesize all the information into a clear, concise final answer.
    Focus only on providing the most relevant information to the user's original question."""
    
    # Create a new model instance without tools for the final response
    curator_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Add system message and invoke with the existing messages
    system_message = SystemMessage(content=curator_prompt)
    
    # Generate the curated response
    all_messages = [system_message] + state.messages
    curated_response = curator_model.invoke(all_messages)
    
    # Add node trace to track flow
    updated_trace = state.node_trace + ["curator"]
    
    return AppState(messages=[curated_response], node_trace=updated_trace)


def output_formatter(state: AppState) -> Dict[str, Any]:
    """Format the final output to only contain the response text.
    
    Note: We return a dictionary here because that's what StateGraph expects.
    The dictionary will be converted to FinalResponse in the main app.
    """
    # Get the final AI message from the state
    final_message = state.messages[-1]
    
    # Convert content to string if it's not already
    content = final_message.content
    if isinstance(content, (list, dict)):
        content = str(content)
    
    # Create a FinalResponse object with just the text content
    result = FinalResponse(
        response=content,
        metadata={"node_trace": state.node_trace + ["output_formatter"]}
    )
    
    # We can also log the node trace for debugging
    print(f"Flow trace: {' -> '.join(state.node_trace + ['output_formatter'])}")
    
    # Return a dictionary that can be properly handled by StateGraph
    return {"messages": [final_message], "final_response": result}

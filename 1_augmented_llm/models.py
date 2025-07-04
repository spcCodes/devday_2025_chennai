from typing import Annotated, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AppState(BaseModel):
    """Base State model for the application.
    
    This model tracks the conversation messages and the flow of nodes
    to provide insight into how the graph is processing information.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    # Track the flow of nodes for debugging and logging
    node_trace: List[str] = Field(default_factory=list)
    # Optional metadata for more complex flows
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class FinalResponse(BaseModel):
    """Model for the final response returned to the user.
    
    This model contains only the essential data that should be returned
    to the user, excluding internal states and metadata.
    """
    response: str
    # Optional metadata fields if needed for the UI
    metadata: Dict[str, Any] = Field(default_factory=dict) 
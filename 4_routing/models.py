from typing_extensions import Literal
from typing import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        default="story", description="The next step in the routing process"
        )
    
# State
class State(TypedDict):
    input: str
    decision: str
    output: str


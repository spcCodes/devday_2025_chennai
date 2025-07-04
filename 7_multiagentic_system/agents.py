from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#custom imports 
from tools import add, multiply , subtract , divide , search_tavily

# Using the correct import for langchain
from langgraph.prebuilt import create_react_agent


#custom imports 
math_agent = create_react_agent(
    model=model,
    tools=[add, multiply, subtract, divide],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[search_tavily],
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import TavilySearchResults

def search_duckduckgo(query: str):
    """Searches DuckDuckGo using LangChain's DuckDuckGoSearchRun tool."""
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

def search_tavily(query: str):
    """Searches Tavily using LangChain's TavilySearchResults tool."""
    search = TavilySearchResults()
    return search.invoke(query)

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


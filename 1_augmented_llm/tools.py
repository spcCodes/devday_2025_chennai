from langchain_core.tools import tool
from datetime import datetime
from typing import List, Dict, Any
import requests


from langchain_community.tools.tavily_search import TavilySearchResults
tavily_tool = TavilySearchResults(max_results=4)

@tool 
def search_web(query:str)->str:
    """Search the web for information"""
    return tavily_tool.run(query)

@tool
def get_current_date()->str:
    """Get the current date"""
    return datetime.now().strftime("%Y-%m-%d")

@tool
def add_numbers(a:int,b:int)->int:
    """Add two numbers together"""
    return a+b

@tool
def subtract_numbers(a:int,b:int)->int:
    """Subtract two numbers"""
    return a-b


@tool
def multiply_numbers(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

@tool
def divide_numbers(a:int,b:int)->float:
    """Divide two numbers"""
    return a/b
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# Internet search tool initialize karein
def get_search_tool():
    return TavilySearchResults(k=3) # Ek waqt mein 3 results layega
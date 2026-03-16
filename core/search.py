import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class ResearchSearch:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def execute_search(self, query: str, depth: str = "advanced"):
        # 'advanced' depth performs a more thorough search for deep research
        response = self.client.search(query=query, search_depth=depth, max_results=5)
        return response['results']
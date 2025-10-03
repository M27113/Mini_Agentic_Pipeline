import os
import sys
from tavily import TavilyClient  

class Actor:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("[Error] TAVILY_API_KEY not set in .env")
            sys.exit(1)
            # added try except for better error handling
        try:
            self.tavily = TavilyClient(api_key=api_key)
        except Exception as e:
            print(f"[Error] Failed to initialize Tavily client: {e}")
            sys.exit(1)
        self.cache = {} # Simple in-memory cache

    def web_search(self, query: str) -> str:
        # added simple in-memory cache for web search results
        if query in self.cache:  # Check cache first
            return self.cache[query]
        
        """
        Executes a web search via Tavily API.
        Returns a concise paragraph (~3-4 lines).
        """
        # added try except for better error handling
        try:
            results = self.tavily.search(query, max_results=3)  # top 3 results
            if results and "results" in results:
                snippets = [r.get("content", "") for r in results["results"]]
                text = " ".join(snippets)
                output = text[:500] + ("..." if len(text) > 500 else "")
                self.cache[query] = output
                return output
            return "No relevant web results found."
        except Exception as e:
            print(f"[Error] Tavily API call failed: {e}")
            return f"Tavily API error: {e}"


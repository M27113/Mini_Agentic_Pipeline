import os
from tavily import TavilyClient  

class Actor:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not set in .env")
        self.tavily = TavilyClient(api_key=api_key)

    def web_search(self, query: str) -> str:
        """
        Executes a web search via Tavily API.
        Returns a concise paragraph (~3-4 lines).
        """
        try:
            results = self.tavily.search(query, max_results=3)  # top 3 results
            if results and "results" in results:
                snippets = [r.get("content", "") for r in results["results"]]
                text = " ".join(snippets)
                return text[:500] + ("..." if len(text) > 500 else "")
            return "No relevant web results found."
        except Exception as e:
            return f"Tavily API error: {e}"

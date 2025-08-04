import requests

class WebSearchAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google"
        }
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        for item in data.get("organic_results", []):
            results.append({"title": item.get("title"), "link": item.get("link")})
        return results
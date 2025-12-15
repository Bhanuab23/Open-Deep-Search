import os
from tavily import TavilyClient

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)

response = client.search(
    query="What is artificial intelligence?",
    search_depth="basic"
)

print(response)

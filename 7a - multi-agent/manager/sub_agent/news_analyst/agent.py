from google.adk.agents import Agent
from google.adk.tools import google_search
import datetime
from dotenv import load_dotenv
load_dotenv()

news_analyst = Agent(
    name="News_Analyst",
    model="gemini-2.0-flash",
    description="An agent that helps users track news articles.",
    instruction="""
        You are a helpful news assistant that helps users track news articles.
        When asked about news articles:
        1. Use the google_search tool to fetch the latest news articles for the requested topic
        2. Format the response to show each article's title, link, and a brief snippet
        3. If no articles are found, mention this in your response  
        Example response format:
        "Here are the latest news articles on [topic]:
        - Title: [Article Title 1]
        Link: [Article Link 1]
        Snippet: [Brief Snippet 1]
        - Title: [Article Title 2]
        Link: [Article Link 2]
        Snippet: [Brief Snippet 2]""",
        tools=[google_search]
)

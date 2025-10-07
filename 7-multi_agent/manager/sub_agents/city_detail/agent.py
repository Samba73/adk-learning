from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


model_name = LiteLlm(model = "ollama/llama3.2")

city_detail_agent = Agent(
    name = "city_detail_agent",
    model = "gemini-2.0-flash",
    description="An agent that provides detailed information about a city.",
    instruction="""
    Provide detailed information about the specified city, 
    including its history, culture, demographics, and notable landmarks.""")
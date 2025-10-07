from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


model_name = LiteLlm(model="ollama/llama3.2")

find_capital_agent = Agent(
    name="find_capital_agent",  
    model="gemini-2.0-flash",
    description="An agent to find the capital of a country",
    instruction="""
        You are a helpful assistant that finds the capital of a country.

        When asked for capital of a country, respond with just the name of the capital city.
        If the user asks about anything else, 
        you should delegate the task to the manager agent.
    """)
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="ollama/llama3.2"
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Why is the sky blue?"}
]

root_agent = Agent(
    name="local_agent",
    model=model,
    description="Local Agent",
    instruction="""
    You are a helpful assistant that can answer questions about various topics.
    Provide clear, accurate, and helpful responses to user queries.
    """
)

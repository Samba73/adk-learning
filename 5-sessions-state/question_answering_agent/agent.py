from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model_name = LiteLlm(model="ollama/llama3.2")

question_answering_agent = Agent(
    name="question_answering_agent",
    model=model_name,
    description="An agent to answer questions about person",
    instruction="""
        You are a helpful assistant that answers question about person preferences.

        Here is some information about the user:
        Name:
        {user_name}
        Preferences:
        {user_preferences}
    """
)
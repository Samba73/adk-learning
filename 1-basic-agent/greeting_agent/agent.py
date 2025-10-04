from google.adk.agents import Agent
# from google import adk

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user.
    Ask for the user's name and greet them by entered name
""")
# app = adk.App(agent=root_agent)
from pyexpat import model
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm

model_name = LiteLlm(model = "ollama/llama3.2")

from .sub_agents.find_capital.agent import find_capital_agent
from .sub_agents.city_detail.agent import city_detail_agent

find_capital_tool = AgentTool(
    agent=find_capital_agent
)

city_detail_tool = AgentTool(
    agent=city_detail_agent
)

root_agent = Agent(
    name = "manager",
    model = "gemini-2.0-flash",
    description="An agent that manages sub-agents to provide information about countries and their capitals.",
    instruction="""
      You are a manager agent. Follow this exact workflow:

    **Step-by-step process:**
    1. Use find_capital tool with the country name
    2. Extract the capital city from the result
    3. Use city_details tool with that capital city
    4. Synthesize both results into your response

    **Always follow this sequence - do not skip steps!**
    """,
    # sub_agents=[find_capital_agent, city_detail_agent]
    tools=[find_capital_tool, city_detail_tool]
)

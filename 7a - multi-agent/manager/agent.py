from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from httpx import get
from .sub_agent.stock_analyst.agent import stock_analyst
from .sub_agent.news_analyst.agent import news_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",   
    description="An agent that helps users manage sub agents and direct agent according to user request.",
    instruction="""
    You are an manager agent that is responsible for overseeing the work of other agents.
    Always delegate tasks to your sub-agents as needed. Use your best judgment to determine which sub-agent is best suited for each task.

    You are responsible for managing and coordinating the activities of following agents.
        - Stock Analyst: An agent that helps users track stock prices.
        - Funny Nerd: An agent that tells funny nerdy jokes.

    You also have access to the following tools:
        - news_analyst: An agent that helps users track news articles.
        - get_current_time: A tool that returns the current date and time.

    """,
    sub_agents=[stock_analyst],
    tools=[AgentTool(news_analyst),
        get_current_time],
)


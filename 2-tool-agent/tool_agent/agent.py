import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time(city:str) -> dict:
    """ Get the current time for new york city sent as argument
        in the format YYYY-MM-DD HH:MM:SS
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:

        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}"
        }
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (f"The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}")
    return {"status": "success", "message": report}

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool Agent",
    instruction="""
    You are a useful agent that can use the following tools:
    - google_search
    """,
    tools=[get_current_time])

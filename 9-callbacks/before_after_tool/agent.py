from importlib import simple
from json import tool
from unittest import runner
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from copy import deepcopy
from google.genai import types
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional


def get_capital_city(country: str) -> str:

    print(f"--- Tool 'get_capital_city' executing with country: {country} ---")
    capitals = {
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "Portugal": "Lisbon",
        "India": "New Delhi",
    }
    return {"result": capitals.get(country)}

capital_tool = FunctionTool(func=get_capital_city)

def simple_before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional [Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"--- Before Tool Callback: Agent '{agent_name}' is about to use Tool '{tool_name}' with input: {args} ---")
    # You can modify tool_input here if needed
    if tool_name == "get_capital_city" and args.get("country", "").lower() == "india":
        print(f"[Callback] Correcting country name from 'india' to 'India'")

        args["country"] = "India"  # Correct the country name
        return None

    if tool_name == "get_capital_city" and args.get("country", "").upper() == "BLOCK":
        print("[Callback] Detected 'BLOCK'. Skipping tool execution.")
        return {"result": "Tool execution was blocked by before_tool_callback."}

    print("[Callback] Proceeding with original or previously modified args.")
    return None

def simple_after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_response: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"--- After Tool Callback: Agent '{agent_name}' used Tool '{tool_name}' with input: {args} and got output: {tool_response} ---")
    # You can modify tool_output here if needed
    if tool_name == "get_capital_city" and "result" in tool_response:
        original_result = tool_response["result"]
        modified_result = f"{original_result} (verified by after_tool_callback)"
        print(f"[Callback] Modifying tool output from '{original_result}' to '{modified_result}'")
        tool_response["result"] = modified_result
    return tool_response
    

root_agent = LlmAgent(
    name="guardrail_agent",
    model="gemini-2.0-flash",
    description="An agent that uses guardrails to ensure safe and appropriate responses.",
    instruction="""
    You are a helpful assistant that adheres to strict guidelines to ensure safe and appropriate responses.
    Always follow the guardrails provided in the tools.
    """,
    tools=[capital_tool],
    before_tool_callback=simple_before_tool_callback,
    after_tool_callback=simple_after_tool_callback

)
APP_NAME = "guardrail_agent_app"
USER_ID = "samba"
SESSION_ID = "session_1"

async def setup_session_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,user_id=USER_ID,session_id=SESSION_ID)
    runner = Runner(agent =llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    
    session, runner = await setup_session_runner()
    content = types.Content(role="user", parts=[types.Part(text=query)])
   
    print(f"\n--- Running Query: {query} ---")
    
    events = runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response =  event.content.parts[0].text.strip()
                print(f"Final Response: {final_response}")

if __name__ == "__main__":
    import asyncio
    query = "What is the refund policy?"
    asyncio.run(call_agent_async(query))               
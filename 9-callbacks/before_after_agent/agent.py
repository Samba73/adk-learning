import time
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from typing import List, Dict, Any, Optional
from google.genai import types
from datetime import datetime


def before_agent_call(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    print(f"--- Before Agent Callback: Agent '{agent_name}' is about to make a call ---")

    state = callback_context.state
    
    timestamp = datetime.now()

    if "agent_name" not in state:
        state["agent_name"]= agent_name
        print(f"[Callback] Agent name from state: {state['agent_name']}")

    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1

    state["request_start_time"] = timestamp
        
        # Log the request
    print("=== AGENT EXECUTION STARTED ===")
    print(f"Request #: {state['request_counter']}")
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Print to console
    print(f"\n[BEFORE CALLBACK] Agent processing request #{state['request_counter']}")

    return None

def after_agent_call(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    print(f"--- After Agent Callback: Agent '{agent_name}' has completed a call ---")

    state = callback_context.state
    timestamp = datetime.now()
    duration = None

    if "request_start_time" not in state:
        duration = (timestamp - state["request_start_time"]).total_seconds()

    
    # Log the completion
    print("=== AGENT EXECUTION COMPLETED ===")
    print(f"Request #: {state.get('request_counter', 'Unknown')}")
    if duration is not None:
        print(f"Duration: {duration:.2f} seconds")

    # Print to console
    print(
        f"[AFTER CALLBACK] Agent completed request #{state.get('request_counter', 'Unknown')}"
    )
    if duration is not None:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")

    return None

root_agent = LlmAgent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="An agent that uses guardrails to ensure safe and appropriate responses.",
    instruction="""
    You are a friendly greeting agent. Your name is {agent_name}.
    
    Your job is to:
    - Greet users politely
    - Respond to basic questions
    - Keep your responses friendly and concise
    """,
    before_agent_callback=before_agent_call,
    after_agent_callback=after_agent_call)


from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models import LlmRequest, LlmResponse
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import List, Dict, Any, Optional
import copy


def simple_before_model_callback(llm_request: LlmRequest, callback_context: CallbackContext) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"--- Before Model Callback: Agent '{agent_name}' is about to make a model request ---")
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        last_user_message = llm_request.contents[-1].parts[0].text
    print(f"Last user message: {last_user_message}")
    # You can modify llm_request here if needed

    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[types.Part(text="")])
    prefix = "[Modified by before_model_callback]"

    if not isinstance(original_instruction, types.Content):
        original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts = [types.Part(text="")]
    modified_text = f"{prefix} {original_instruction.parts[0].text}"
    modified_instruction = modified_text
    llm_request.config.system_instruction = modified_instruction
    print(f"Modified system instruction: {modified_instruction}")
        # Example: Block requests containing the word "cut"
        
    if "cut" in last_user_message.lower():
        print(f"[Callback] Blocking model call due to 'cut' in user message.")
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text="Model call was blocked by before_model_callback.")]),
        )

def simple_after_model_callback(llm_response: LlmResponse, callback_context: CallbackContext) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"--- After Model Callback: Agent '{agent_name}' received a model response ---")
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_response = llm_response.content.parts[0].text
        elif llm_response.content.parts[0].function_call:
            print(f"[Callback] Inspected response: Contains function call '{llm_response.content.parts[0].function_call.name}'. No text modification.")
            return None
        else:
            print("[Callback] Inspected response: No text content found.")
            return None   
    elif llm_response.error_message:
        print(f"[Callback] Inspected response: Error message '{llm_response.error_message}'. No text modification.")
        return None
    else:
        print("[Callback] Inspected response: No content found.")
        return None
    
    search_term = "joke"
    replace_term = "funny story"
    if search_term in original_response.lower():
        modified_response = original_response.lower().replace(search_term, replace_term)
        modified_response = modified_response.replace(search_term.capitalize(), replace_term.capitalize())
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = modified_response
        print(f"[Callback] Modifying response from '{original_response}' to '{modified_response}'")
        llm_response.content.parts[0].text = modified_response
        new_response = LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata)
        return new_response
    else:
        print("[Callback] No modifications made to the response.")
        return None    
            

root_agent = LlmAgent(
    name="RootAgent",
    description="An LLM agent demonstrating before and after model callbacks.",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    before_model_callback=simple_before_model_callback,
    after_model_callback=simple_after_model_callback
)

APP_Name = "guardrail_app"
USER_ID = "samba"
SESSION_ID = "session_1"

async def setup_sesssion_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_Name,user_id=USER_ID,session_id=SESSION_ID)    
    runner = Runner(agent =root_agent, app_name=APP_Name, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    """Call the agent asynchronously with the user's message."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_sesssion_and_runner()
    print(f"\n--- Running Query: {query} ---")

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response =  event.content.parts[0].text.strip()
                print(f"Final Response: {final_response}")



if __name__ == "__main__":   
    import asyncio
    asyncio.run(call_agent_async)

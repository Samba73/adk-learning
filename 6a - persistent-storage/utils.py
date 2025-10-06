from google.genai import types

async def process_agent_response(event):
    """Process the agent's response event and extract the final response text."""
    
    final_response = None

    # Log the event details for debugging
    # print(f"--- Agent Event: {event.type} ---")
    print(f"--- Event ID: {event.id}, Author: {event.author} ---")
    if event.is_final_response():
        if event.content and event.content.parts:
            final_response =  event.content.parts[0].text.strip()
    return final_response


async def call_agent_async(runner, session_id: str, user_message: str):
    
    """Call the agent asynchronously with the user's message."""
    content = types.Content(role="user", parts=[types.Part(text=user_message)])
   
    print(f"\n--- Running Query: {user_message} ---")
    
    final_response = None

    try:
        async for event in runner.run_async(
            user_id="samba73", session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    return final_response
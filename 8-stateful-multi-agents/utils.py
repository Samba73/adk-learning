from google.genai import types
from datetime import datetime

async def update_integration_history(app_name, user_id, session_id, entry, session_service):
    """
    Updates the integration history in the session state with the latest response.
    """
    try:
        session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        if not session:
            print(f"No session found for app: {app_name}, user: {user_id}, session: {session_id}")
            return

        interaction_history = session.state.get("interaction_history", [])

        # Add a timestamp to the entry
        entry["timestamp"] = datetime.utcnow().isoformat() + "Z"

        interaction_history.append(entry)
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history 

        # Update the session state
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state
        )
    except Exception as e:
        print(f"Error updating integration history: {e}")    


async def add_user_history(app_name, user_id, session_id, user_input, session_service):
    """
    Adds user input to the interaction history in the session state.
    """
    await update_integration_history(app_name, user_id, session_id, 
                               {"action": "user_query", "query": user_input}, session_service)

async def add_agent_response(app_name, user_id, session_id, agent_name, response, session_service):
    """
    Adds agent response to the interaction history in the session state.
    """
    await update_integration_history(app_name, user_id, session_id, 
                               {"action": "agent_response", "agent": agent_name, "response": response}, 
                               session_service)

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


async def call_agent_async(runner, user_id, session_id: str, user_message: str):
    
    """Call the agent asynchronously with the user's message."""
    content = types.Content(role="user", parts=[types.Part(text=user_message)])
   
    print(f"\n--- Running Query: {user_message} ---")
    
    final_response = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.author:
                print(f"Event Author: {event.author}")
                agent_name = event.author
            response = await process_agent_response(event)
            if response:
                final_response = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    if response and agent_name:
        await update_integration_history(runner.app_name, user_id, session_id,
                                   {"action": "agent_response", "agent": agent_name, "response": response}, 
                                   runner.session_service)


    return final_response
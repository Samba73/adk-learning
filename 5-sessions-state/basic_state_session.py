from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types
import uuid
import asyncio
from question_answering_agent.agent import question_answering_agent

initial_state ={
        "user_name": "Samba",
        "user_preferences": """
            I like to play cricket, Pickleball, Tennis and Football
            My favorite food is south indian
            My favorite TV show is Kattu Karuppu
            My favorite movie is Godfather
        """
    }
async def main():
    session_service = InMemorySessionService()
    
    APP_NAME = "Samba Bot"
    USER_ID = "Samba K"
    SESSION_ID = str(uuid.uuid4())
    
    session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_state
        )
    print("Session Created")
    print(f"\tSession ID: {SESSION_ID}")

    # agent_instance = question_answering_agent(initial_state["user_name"], initial_state["user_preferences"])
    # print(agent_instance)
    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    new_message = types.Content(
            role="user",
            parts=[types.Part(text="What is Samba's favorite tv show")]          
        )

    print("=== Running Agent ===")
    async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    # final_response_text = event.content.parts[0].text
                    print(event.content)
                    print(f"Final Response is : {event.content.parts[0].text}")
                elif event.actions and event.actions.escalate:
                    # final_response_text = f"Agent escalated: {event.error_message or 'No Specific message'}"    
                    print(f"Escalation: {event.error_message}")
                break
            # print(f"<<< Agent Resopnse: {final_response_text}")
    print("=== Session Event Exploration ===")
    event_session = await session_service.get_session(
         app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print("=== Session Messages ===")
    for k,v in event_session.state.items():
         print(f"{k}: {v}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occured: {e}")                

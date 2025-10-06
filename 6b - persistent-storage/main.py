from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from vertexai import init
from memory_agent.agent import memory_agent
import asyncio
import uuid
from dotenv import load_dotenv
from utils import call_agent_async

load_dotenv()
db_url = "sqlite:///memory_agent_sessions.db"

async def main():
    # Initialize session service with SQLite database
    session_service = DatabaseSessionService(db_url=db_url)

    user_name = input( "Enter your name: " ).strip()
    if not user_name:
        user_name = "guest"
    # id = str(uuid.uuid4())   
    user_id = f"{user_name.lower()}"


    # Define initial state for sessions
    initial_state = {
        "user_name": user_name,
        "reminders": [],
    }

    APP_NAME = "Memory Agent"
    USER_ID = user_id

    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,  
        user_id=USER_ID,
    )
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=memory_agent, 
        app_name=APP_NAME,
        session_service=session_service,
    )

    print(f"\nWelcome to Memory Agent Chat, {user_name}!")
    print("Type 'exit' to quit.\n") 
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat. Goodbye!")
            break
        # print(f"session id: {SESSION_ID}")    
        response = await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
        if response:
            print(f"Agent: {response}")
        else:
            print("Agent did not respond. Please try again.")   
            print("Agent: [No response received]")

if __name__ == "__main__":
    asyncio.run(main())
from google.adk.sessions import InMemorySessionService
from customer_service_agent.agent import customer_service_agent
from google.adk.runners import Runner
from dotenv import load_dotenv
from utils import call_agent_async, add_user_history
import asyncio

load_dotenv()

session_service = InMemorySessionService()

initial_state = {
    "user_name": "samba",
    "purchased_courses": [],
    "interaction_history": []   
}

async def main():
    APP_NAME = "Customer Service Agent"
    USER_ID = "samba"
    
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print(f"\nWelcome to the Customer Service Agent Chat, {initial_state['user_name']}!")
    print("Type 'exit or quit' to quit.\n")
    while True:
        user_input = input(f"{initial_state['user_name']}: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        
        await add_user_history(APP_NAME, USER_ID, SESSION_ID, user_input, session_service)

        response = await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())

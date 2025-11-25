from agents.website_builder_simple.agent import root_agent
from google.ask.sessions import InMemorySessionService
from google.genai.types import Content, Part
from google.adk.runners import Runner
from dotenv import load_dotenv
from rich import print as rprint
from typing import Any
import asyncio
import json


load_dotenv()

APP_NAME = "website_builder_simple"
USER_ID = "user_id"
SESSION_ID = "session_id"

async def chat_loop():
    session_service = InMemorySessionService()

    session = await session_service.create_session(APP_NAME, USER_ID, SESSION_ID)
    runner = Runner(
                agent=root_agent,
                app_name=APP_NAME,
                session_service=session_service,
            )
    

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Goodbye!")
        break
    new_message = Content(role='user', parts=[Part(text=user_input)])
    
    events = await runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        message=new_message,
    )

    final_response = ""
    i=0
    async for event in events:
        i+=1
        print_json_response(event, f"============Event #{i}=============")
        if hasattr(event, "author") and event.author == "code_writer_agent":
            if event.is_final_response():
                final_response = event.content.parts[0].text
                print(f"\nAgent Response:\n------------------------\n{final_response}\n")
                break

    def print_json_response(event: Any, message: str) -> None:
        print(f"\n=== {message} ===")       
        try:
            if hasattr(event, "root"):
                data = event.root.model_dump(mode='json', exclude_none=True)
                print(json.dumps(data, indent=2))
            else:
                data = event.model_dump(mode='json', exclude_none=True)
                print(json.dumps(data, indent=2))
        except Exception as e:
            rprint(f"[red bold]Error printing JSON:[/red bold] {e}")
            rprint(repr(event))
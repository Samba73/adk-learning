from unittest.mock import Base
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field

class EmailContent(BaseModel):
    """structure the output from agent (llm) in the format specified below 
    and mapped to agent"""
    subject: str = Field(description="The subject line of the email. Should be concise and descriptive")
    body:str = Field(description="""The main content of the email. Should be well-formatted with proper" \
                    greeting, paragraphs and signature""")
    
model_name = LiteLlm(
    model="ollama/llama3.2"
)    

root_agent = Agent(
    name="email_agent",
    model=model_name,
    description="Email Agent",
    instruction="""
        You are Email Generation Assistant.
        Your task of to generate a professional email based on user's request.

        GUIDELINES:
        - Create an appropriate subject line(concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and Concise main content
            * Appropriate Closing
            * Your name in signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep email concise and complete

        IMPORTANT: Your response MUST be valid JSON matching the following structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting"
        }    

        DO NOT include any explanation of additional texts outside the JSON response

        """,
        output_schema=EmailContent,
        output_key="email"
)
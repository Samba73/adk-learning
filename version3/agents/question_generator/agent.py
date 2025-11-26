import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm
from utils.file_loader import load_file

load_dotenv()
model_name = LiteLlm(
    model="ollama/llama3.2"
) 

question_generator_agent = LlmAgent(
    name="question_generator_agent",
    model="gemini-2.0-flash",
    description=load_file(
        "agents/requirements_writer/description.txt",),
    instruction=load_file(
        "agents/requirements_writer/instruction.txt",),
    output_key="questions_output",
    tools=[google_search]
)
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from google.adk.agents import LlmAgent, Agent
from google.adk.models.lite_llm import LiteLlm
from utils.file_loader import load_file

model_name = LiteLlm(
    model="ollama/llama3.2"
) 

query_generator_agent = LlmAgent(
    name="query_generator_agent",
    model="gemini-2.0-flash",
    description=load_file(
        "agents/requirements_writer/description.txt",),
    instruction=load_file(
        "agents/requirements_writer/instruction.txt",),
    output_key="query_output"
)
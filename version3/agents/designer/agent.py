import os
import sys
from xml.parsers.expat import model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from google.adk.agents import LlmAgent, Agent
from google.adk.models.lite_llm import LiteLlm
from utils.file_loader import load_file

model_name = LiteLlm(
    model="ollama/llama3.2"
) 

designer_agent = LlmAgent(
    name="designer_agent",
    model="gemini-2.0-flash",
    description=load_file(
        "agents/designer/description.txt",),
    instruction=load_file(
        "agents/designer/instruction.txt",),
    output_key="design_document"
)
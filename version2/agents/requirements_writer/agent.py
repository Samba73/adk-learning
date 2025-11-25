import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from google.adk.agents import LlmAgent
from utils.file_loader import load_file

requirements_writer_agent = LlmAgent(
    name="requirements_writer_agent",
    model="gemini-2.0-flash",
    description=load_file(
        "agents/requirements_writer/description.txt",),
    instruction=load_file(
        "agents/requirements_writer/instruction.txt",),
    output_key="requirements_document"
)
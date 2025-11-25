import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from google.adk.agents import LlmAgent
from tools.file_writer_tool import write_to_file
from utils.file_loader import load_file
code_writer_agent = LlmAgent(
    name="code_writer_agent",
    model="gemini-2.0-flash",
    description=load_file(
        "agents/code_writer/description.txt",),
    instruction=load_file(
        "agents/code_writer/instruction.txt",),
    tools=[write_to_file]
)
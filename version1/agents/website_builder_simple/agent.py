import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from tools.file_writer_tool import write_to_file
from utils.file_loader import load_file
from google.adk.agents import LlmAgent


root_agent = LlmAgent(
    name="website_builder_simple",
    model="gemini-2.0-flash",
    description=load_file("description.txt"),
    instruction=load_file("instruction.txt"),
    tools=[write_to_file])
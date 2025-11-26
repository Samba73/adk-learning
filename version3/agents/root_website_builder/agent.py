from google.adk.agents import SequentialAgent
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from requirements_writer.agent import requirements_writer_agent
from designer.agent import designer_agent
from code_writer.agent import code_writer_agent
from question_generator.agent import question_generator_agent
from query_generator.agent import query_generator_agent 
from questions_researcher.agent import questions_researcher_agent
from utils.file_loader import load_file

root_agent = SequentialAgent(
    name="root_website_builder_agent",
    sub_agents=[
        question_generator_agent, 
        questions_researcher_agent, 
        query_generator_agent, 
        requirements_writer_agent, 
        designer_agent, 
        code_writer_agent],
    description=load_file(
        "agents/root_website_builder/description.txt"))
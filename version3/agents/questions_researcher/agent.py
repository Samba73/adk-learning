from json import tool
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search
from utils.file_loader import load_file

load_dotenv()

base_intructions = load_file(
    "agents/questions_researcher/instruction.txt")
base_descriptions = load_file(
    "agents/questions_researcher/description.txt")

model_name = LiteLlm(
    model="ollama/llama3.2"
) 

questions_researcher_agent_1 = LlmAgent(
    name="questions_researcher_agent_1",
    model="gemini-2.0-flash",
    description=f'{base_descriptions} This agent is responsible for researching answers to Question Number 1 only.',
    instruction=f'You are assigned to research answers to the Question Number 1 only.\n\n {base_intructions}    ',
    output_key="question_1_research_output",
    tools=[google_search]
)
questions_researcher_agent_2 = LlmAgent(
    name="questions_researcher_agent_2",
    model="gemini-2.0-flash",
    description=f'{base_descriptions} This agent is responsible for researching answers to Question Number 2 only.',
    instruction=f'You are assigned to research answers to the Question Number 2 only.\n\n {base_intructions}    ',
    output_key="question_2_research_output",
    tools=[google_search]
)
questions_researcher_agent_3 = LlmAgent(
    name="questions_researcher_agent_3",
    model="gemini-2.0-flash",
    description=f'{base_descriptions} This agent is responsible for researching answers to Question Number 3 only.',
    instruction=f'You are assigned to research answers to the Question Number 3 only.\n\n {base_intructions}    ',
    output_key="question_3_research_output",
    tools=[google_search]
)
questions_researcher_agent_4 = LlmAgent(
    name="questions_researcher_agent_4",
    model="gemini-2.0-flash",
    description=f'{base_descriptions} This agent is responsible for researching answers to Question Number 4 only.',
    instruction=f'You are assigned to research answers to the Question Number 4 only.\n\n {base_intructions}    ',
    output_key="question_4_research_output",
    tools=[google_search]
)
questions_researcher_agent_5 = LlmAgent(
    name="questions_researcher_agent_5",
    model="gemini-2.0-flash",
    description=f'{base_descriptions} This agent is responsible for researching answers to Question Number 5 only.',
    instruction=f'You are assigned to research answers to the Question Number 5 only.\n\n {base_intructions}    ',
    output_key="question_5_research_output",
    tools=[google_search]
)

parallel_questions_researcher_agent = ParallelAgent(
    name="parallel_questions_researcher_agent",  
    sub_agents=[
        questions_researcher_agent_1,
        questions_researcher_agent_2,
        questions_researcher_agent_3,
        questions_researcher_agent_4,
        questions_researcher_agent_5,
    ],
    description="Runs five research agents in parallel to research answers to five different questions.")

questions_researcher_agent = parallel_questions_researcher_agent
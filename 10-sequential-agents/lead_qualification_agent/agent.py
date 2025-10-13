from google.adk.agents import SequentialAgent

from .sub_agents.recommender.agent import action_recommender_agent  
from .sub_agents.scorer.agent import scorer_agent
from .sub_agents.validator.agent import validator_agent

root_agent = SequentialAgent(
    name="RootSequentialAgent",
    sub_agents=[
        scorer_agent,
        validator_agent,
        action_recommender_agent
    ],
    description="An agent that recommends actions, scores them, and validates them in sequence.")
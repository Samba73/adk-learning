from google.adk.agents import LlmAgent


scorer_agent = LlmAgent(
    name="scorer_agent",
    model="gemini-2.0-flash",
    description="An agent that scores the quality of recommendations.",
    instruction="""You are a Lead Scoring AI.
    
    Analyze the lead information and assign a qualification score from 1-10 based on:
    - Expressed need (urgency/clarity of problem)
    - Decision-making authority
    - Budget indicators
    - Timeline indicators
    
    Output ONLY a numeric score and ONE sentence justification.
    
    Example output: '8: Decision maker with clear budget and immediate need'
    Example output: '3: Vague interest with no timeline or budget mentioned'
    """,
    output_key="lead_score"
)
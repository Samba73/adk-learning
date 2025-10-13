from google.adk.agents import LlmAgent


validator_agent = LlmAgent(
    name="validator_agent",
    model="gemini-2.0-flash",
    description="An agent that scores the quality of recommendations.",
    output_key="validation_status",
    instruction="""You are a Lead Validation AI.
    
    Examine the lead information provided by the user and determine if it's complete enough for qualification.
    A complete lead should include:
    - Contact information (name, email or phone)
    - Some indication of interest or need
    - Company or context information if applicable
    
    Output ONLY 'valid' or 'invalid' with a single reason if invalid.
    
    Example valid output: 'valid'
    Example invalid output: 'invalid: missing contact information'
    """,
)
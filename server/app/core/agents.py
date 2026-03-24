import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from exa_py import Exa

# Absolute imports from your new structure
from app.agents.vibe_agent import VibeAgent
from app.agents.scouting_agent import ScoutingAgent
from app.agents.choice_agent import ChoiceAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.integrations.wheather_client import WheatherClient

load_dotenv()

# 1. Initialize the raw API clients (The Singletons)
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
exa_client = Exa(api_key=os.getenv("EXA_AI_API_KEY"))
wheather_client = WheatherClient()  # For real-time weather data in the ReviewerAgent

# 2. Initialize the Agent Objects
# These are the "Brains" that LiveKit will call
vibe_agent = VibeAgent(openai_client, model="gpt-4o")
scout_agent = ScoutingAgent(exa_client)
choice_agent = ChoiceAgent(openai_client)
reviewer_agent = ReviewerAgent(openai_client, wheather_client)

# 3. The "Master Workflow" 
# This is what LiveKit calls when the user finishes speaking
async def run_remy_workflow(user_transcript: str, user_context: dict):
    """
    The full 'Remy' pipeline: 
    Vibe -> Scout -> Choice -> Review
    """
    # Step 1: Understand the vibe
    vibe = await vibe_agent.run(user_transcript, user_context)
    
    # Step 2: Find 5-10 options in Rexburg/Idaho Falls
    raw_results = await scout_agent.run(vibe.tags, location=user_context.get("location", "Rexburg, ID"))
    
    # Step 3: Pick the best one based on user history/preferences
    top_choice = await choice_agent.run(vibe, raw_results)
    
    # Step 4: Final safety/weather/hours check
    final_plan = await reviewer_agent.run(vibe, raw_results, top_choice, user_context)
    
    return final_plan
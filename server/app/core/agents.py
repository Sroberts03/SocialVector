import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from exa_py import Exa
from app.agents.vibe_agent import VibeAgent
from app.agents.scouting_agent import ScoutingAgent
from app.agents.choice_agent import ChoiceAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.integrations.open_weather import OpenWeather
from app.core.location import Location
from app.integrations.google_maps import GoogleMapsClient
from app.core.weather_service import WeatherService

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
exa_client = Exa(api_key=os.getenv("EXA_AI_API_KEY"))
google_maps_client = GoogleMapsClient(api_key=os.getenv("GOOGLE_MAPS_API_KEY"))  
location = Location(google_maps_client)
open_weather = OpenWeather(api_key=os.getenv("OPENWEATHER_API_KEY"), base_url=os.getenv("OPENWEATHER_BASE_URL"))
weather = WeatherService(open_weather)


vibe_agent = VibeAgent(openai_client, model="gpt-4o")
scout_agent = ScoutingAgent(exa_client)
choice_agent = ChoiceAgent(openai_client, model="gpt-4o")
reviewer_agent = ReviewerAgent(openai_client, weather)

async def run_remy_workflow(user_transcript: str, user_context: dict, latitude: float = None, longitude: float = None):
    """
    The full 'Remy' pipeline: 
    Vibe -> Scout -> Choice -> Review
    """
    try:
        location_info = await location.get_location_info(user_context, latitude, longitude)
    except Exception as e:
        print(f"Error getting location info: {e}")
        

    # Step 1: Understand the vibe
    vibe = await vibe_agent.run(user_transcript, location_info)
    
    # Step 2: Find 5-10 options in Rexburg/Idaho Falls
    raw_results = await scout_agent.run(vibe, location_info)
    
    # Step 3: Pick the best one based on user history/preferences
    top_choice = await choice_agent.run(vibe, raw_results, location_info)
    
    # Step 4: Final safety/weather/hours check
    final_plan = await reviewer_agent.run(vibe, top_choice, location_info)
    
    return final_plan
from datetime import datetime
from openai import AsyncOpenAI
from app.models.schemas import FinalActivity, FinalReview, LocationInfo, VibeSchema
from app.integrations.wheather_client import WheatherClient
from app.prompts.agent_prompts import REVIEWER_SYSTEM_PROMPT

class ReviewerAgent:
    def __init__(self, openai_client, weather_client, model="gpt-4o-mini"):
        self.openai = openai_client
        self.weather = weather_client
        self.model = model

    async def run(self, vibe: VibeSchema, top_choice: FinalActivity, location: LocationInfo) -> FinalReview:
        # 1. Get real data from your WeatherClient
        weather_data = await self.weather.get_weather(location.formatted_address)
        temp = weather_data.get("temp", "unknown") if weather_data else "unknown"
        condition = weather_data.get("condition", "unknown") if weather_data else "unknown"
        description = weather_data.get("description", "unknown conditions") if weather_data else "unknown conditions"
        
        # 2. Format the prompt with location AND weather
        system_msg = REVIEWER_SYSTEM_PROMPT.format(
            city=location.city,
            state=location.state,
            formatted_address=location.formatted_address,
            lat=location.lat,
            lon=location.lon,
            is_precise=location.is_precise,
            temp=temp,
            condition=condition,
            description=description,
            time_for_activity=vibe.time_for_activity,
            energy_level=vibe.energy_level,
            environment_pref=vibe.environment_pref,
            tags=", ".join(vibe.tags)
        )
        
        # 3. Call OpenAI (using a fast model for the final check)
        response = await self.openai.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Review this plan: {top_choice.name}"}
            ],
            response_format=FinalReview
        )
        
        return response.choices[0].message.parsed
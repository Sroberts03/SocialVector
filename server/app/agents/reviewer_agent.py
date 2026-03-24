from openai import AsyncOpenAI
from app.models.schemas import FinalActivity
from app.integrations.wheather_client import WheatherClient
from app.prompts.agent_prompts import REVIEWER_SYSTEM_PROMPT

class ReviewerAgent:
    def __init__(self, openai_client, weather_client, model="gpt-4o-mini"):
        self.openai = openai_client
        self.weather = weather_client
        self.model = model

    async def run(self, choice_name, location="Rexburg"):
        # 1. Get real data from your WeatherClient
        weather_data = await self.weather.get_weather(location)
        
        # 2. Format the prompt with location AND weather
        system_msg = REVIEWER_SYSTEM_PROMPT.format(
            location=location,
            temp=weather_data["temp"],
            condition=weather_data["condition"],
            description=weather_data["description"]
        )
        
        # 3. Call OpenAI (using a fast model for the final check)
        response = await self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Review this plan: {choice_name}"}
            ],
            response_format={ "type": "json_object" } # Ensure we get JSON back
        )
        
        return response.choices[0].message.content
from datetime import datetime
from openai import AsyncOpenAI
from app.models.schemas import FinalActivity, ActivityCandidate, LocationInfo, VibeSchema
from app.prompts.agent_prompts import CHOICE_SYSTEM_PROMPT, CHOICE_USER_INPUT
from typing import List

class ChoiceAgent:
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    async def run(self, vibe: VibeSchema, candidates: List[ActivityCandidate], location: LocationInfo) -> FinalActivity:
        # 1. Format the candidates into a readable list for the LLM
        list_str = "\n".join([f"- {c.name}: {c.description}" for c in candidates])
        
        # 2. Inject data into the templates
        system_msg = CHOICE_SYSTEM_PROMPT.format(
            energy_level=vibe.energy_level,
            environment_pref=vibe.environment_pref,
            time_for_activity=vibe.time_for_activity,
            tags=", ".join(vibe.tags),
            city=location.city,
            state=location.state,
            formatted_address=location.formatted_address,
            lat=location.lat,
            lon=location.lon,
            is_precise=location.is_precise
        )

        user_msg = CHOICE_USER_INPUT.format(
            formatted_address=location.formatted_address,
            candidates_list=list_str,
            time_for_activity=vibe.time_for_activity
        )
        

        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format=FinalActivity,
        )
        return response.choices[0].message.parsed
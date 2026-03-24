from openai import AsyncOpenAI
from app.models.schemas import FinalActivity, ActivityCandidate, VibeSchema
from app.prompts.agent_prompts import CHOICE_SYSTEM_PROMPT, CHOICE_USER_INPUT
from typing import List

class ChoiceAgent:
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    async def run(self, vibe, candidates, location="Rexburg"):
        # 1. Format the candidates into a readable list for the LLM
        list_str = "\n".join([f"- {c.name}: {c.description}" for c in candidates])
        
        # 2. Inject data into the templates
        system_msg = CHOICE_SYSTEM_PROMPT.format(
            energy_level=vibe.energy_level,
            environment_pref=vibe.environment_pref,
            tags=", ".join(vibe.tags)
        )
        
        user_msg = CHOICE_USER_INPUT.format(
            location=location,
            candidates_list=list_str
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
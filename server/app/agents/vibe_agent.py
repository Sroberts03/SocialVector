#Only Job is to take the users input and create a vibe schema
from app.models.schemas import VibeSchema
from app.prompts.agent_prompts import VIBE_SYSTEM_PROMPT as system_prompt
from .base_agent import BaseAgent

class VibeAgent(BaseAgent):
    async def run(self, user_voice_text: str, current_location: str) -> VibeSchema:
        # 1. Prepare the system prompt by filling in the {context}
        formatted_system_prompt = system_prompt.format(context=current_location)
        
        # 2. Prepare the user content
        user_content = f"The user just said: '{user_voice_text}'"
        
        # 3. Hand it off to the base agent to get the structured JSON
        return await self.get_structured_response(
            formatted_system_prompt, 
            user_content, 
            VibeSchema
        )
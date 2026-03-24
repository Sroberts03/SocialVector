import asyncio
import json
from dotenv import load_dotenv
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli, function_tool
from livekit.plugins.openai import LLM, TTS
from livekit.plugins.deepgram import STT
from app.core.agents import run_remy_workflow
from app.models.schemas import FinalReview

load_dotenv()

class Remy(Agent):
    def __init__(self, latitude: float = None, longitude: float = None):
        super().__init__(
            instructions="You are Remy, a helpful social planning assistant. When users ask for recommendations or plans for what to do, call get_social_plan."
        )
        self.user_latitude = latitude
        self.user_longitude = longitude

    @function_tool
    async def get_social_plan(self, user_input: str) -> str:
        """Call this when the user wants a recommendation or plan for what to do."""
        result = await run_remy_workflow(
            user_input, 
            latitude=self.user_latitude, 
            longitude=self.user_longitude, 
            user_context={"city": "Rexburg", "state": "ID"}
        )
        return result.model_dump_json() if isinstance(result, FinalReview) else str(result)

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    latitude = None
    longitude = None
    
    # Wait a moment for participants to fully connect
    await asyncio.sleep(0.5)
    
    participants = list(ctx.room.remote_participants.values())
    if participants:
        participant = participants[0]
        if participant.metadata:
            try:
                metadata = json.loads(participant.metadata)
                latitude = metadata.get('latitude')
                longitude = metadata.get('longitude')
                print(f"User location: lat={latitude}, lon={longitude}")  # Debug log
            except json.JSONDecodeError as e:
                print(f"Failed to parse participant metadata: {e}")
    else:
        print("No participants found, location will be None")
    
    session = AgentSession(
        stt=STT(),
        llm=LLM(model="gpt-4o"),
        tts=TTS(voice="onyx"),
    )
    
    await session.start(agent=Remy(latitude=latitude, longitude=longitude), room=ctx.room)
    await session.say("Hey! I'm Remy. What can I get started for you?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="remy"
    ))
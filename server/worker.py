import asyncio
from dotenv import load_dotenv
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli, function_tool
from livekit.plugins.openai import LLM
from livekit.plugins.deepgram import STT
from livekit.plugins.elevenlabs import TTS
from app.core.agents import vibe_agent, scout_agent, choice_agent, reviewer_agent

load_dotenv()

class Remy(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are Remy, a helpful social planning assistant. When users ask for recommendations or plans for what to do, call get_social_plan."
        )

    @function_tool
    async def get_social_plan(self, user_input: str, location: str = "Rexburg, ID"):
        """Call this when the user wants a recommendation or plan for what to do."""
        print(f"🕵️ Remy thinking... Input: {user_input}")
        vibe = await vibe_agent.run(user_input, location)
        candidates = await scout_agent.run(vibe, location)
        choice = await choice_agent.run(vibe, candidates)
        review = await reviewer_agent.run(choice.name, location)
        return f"I suggest {choice.name}. {review}"


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=STT(),
        llm=LLM(model="gpt-4o"),
        tts=TTS(voice_id="pNInz6obpgDQGcFmaJgB"),
    )

    await session.start(agent=Remy(), room=ctx.room)
    await session.say("Yo! I'm Remy — your go-to for finding something fun to do. What's the vibe?")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="remy"
    ))
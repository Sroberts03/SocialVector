import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.vibe_agent import VibeAgent
from app.models.schemas import VibeSchema

# Additional imports for other agents
from app.agents.choice_agent import ChoiceAgent
from app.agents.scouting_agent import ScoutingAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.models.schemas import ActivityCandidate, FinalActivity, FinalReview

@pytest.mark.asyncio
async def test_vibe_agent_logic():
    # 1. Mock the OpenAI Client so we don't call the real API
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    # Fake the structured output from OpenAI
    mock_response.choices[0].message.parsed = VibeSchema(
        energy_level="High",
        social_intent="Large Crowd",
        environment_pref="Outdoor",
        tags=["basketball", "sports"],
        reasoning="User mentioned wanting to play ball."
    )
    
    # Make the call return our fake response
    mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_response)

    # 2. Run the Agent
    agent = VibeAgent(client=mock_client, model="gpt-4o")
    result = await agent.run("I want to hoop with some people", {"time": "4pm"})

    # 3. Assertions (The "Test")
    assert result.energy_level == "High"
    assert "basketball" in result.tags
    print("✅ VibeAgent logic passed!")


# ------------------- ChoiceAgent Test -------------------
@pytest.mark.asyncio
async def test_choice_agent_logic():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_final_activity = FinalActivity(
        name="Basketball Game",
        description="A fun basketball game at the park",
        location_name="Central Park",
        url="http://example.com",
        category="activity",
        lat=40.0,
        lon=-73.0,
        start_time="2026-03-24T16:00:00",
        weather_ok=True,
        review_status="Looks good!"
    )
    mock_response.choices[0].message.parsed = mock_final_activity
    mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_response)

    agent = ChoiceAgent(client=mock_client, model="gpt-4o")
    vibe = VibeSchema(
        energy_level="High",
        social_intent="Large Crowd",
        environment_pref="Outdoor",
        tags=["basketball", "sports"],
        reasoning="User wants to play basketball."
    )
    candidates = [
        ActivityCandidate(
            name="Basketball Game",
            description="A fun basketball game at the park",
            location_name="Central Park",
            url="http://example.com",
            category="activity"
        )
    ]
    result = await agent.run(vibe, candidates, "Central Park")
    assert result.name == "Basketball Game"
    assert result.weather_ok is True
    print("✅ ChoiceAgent logic passed!")


# ------------------- ScoutingAgent Test -------------------
@pytest.mark.asyncio
async def test_scouting_agent_logic():
    mock_exa = MagicMock()
    mock_result = MagicMock()
    mock_result.title = "Basketball Court"
    mock_result.summary = "Outdoor basketball court."
    mock_result.url = "http://example.com/court"
    mock_result.score = 0.95
    mock_exa.search.return_value.results = [mock_result]

    agent = ScoutingAgent(exa_client=mock_exa)
    vibe = VibeSchema(
        energy_level="High",
        social_intent="Large Crowd",
        environment_pref="Outdoor",
        tags=["basketball"],
        reasoning="Looking for a place to play."
    )
    candidates = await agent.run(vibe, "Central Park")
    assert len(candidates) == 1
    assert candidates[0].name == "Basketball Court"
    print("✅ ScoutingAgent logic passed!")


# ------------------- ReviewerAgent Test -------------------
@pytest.mark.asyncio
async def test_reviewer_agent_logic():
    mock_openai = MagicMock()
    mock_weather = MagicMock()
    mock_response = MagicMock()
    mock_final_review = FinalReview(
        status="PASS",
        reason=None,
        adjustment=None
    )
    mock_response.choices[0].message.parsed = mock_final_review
    mock_openai.chat.completions.create = AsyncMock(return_value=mock_response)
    mock_weather.get_weather = AsyncMock(return_value={
        "temp": 70,
        "condition": "Sunny",
        "description": "Clear skies"
    })

    agent = ReviewerAgent(openai_client=mock_openai, weather_client=mock_weather, model="gpt-4o-mini")
    vibe = VibeSchema(
        energy_level="High",
        social_intent="Large Crowd",
        environment_pref="Outdoor",
        tags=["basketball"],
        reasoning="Looking for a place to play."
    )
    top_choice = FinalActivity(
        name="Basketball Game",
        description="A fun basketball game at the park",
        location_name="Central Park",
        url="http://example.com",
        category="activity",
        lat=40.0,
        lon=-73.0,
        start_time="2026-03-24T16:00:00",
        weather_ok=True,
        review_status="Looks good!"
    )
    user_context = {"user": "test"}
    result = await agent.run(vibe, top_choice, "Central Park", user_context)
    assert result.status == "PASS"
    print("✅ ReviewerAgent logic passed!")
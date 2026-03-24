import pytest
from unittest.mock import AsyncMock, MagicMock
from agents.vibe_agent import VibeAgent
from models.schemas import VibeSchema

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
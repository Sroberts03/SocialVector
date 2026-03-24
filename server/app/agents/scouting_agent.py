from exa_py import Exa
from typing import List
from app.models.schemas import ActivityCandidate, VibeSchema

class ScoutingAgent:
    def __init__(self, exa_client: Exa):
        # We pass the client initialized in agents.py (the singleton)
        self.exa = exa_client

    async def run(self, vibe: VibeSchema, location: str = "Rexburg, ID") -> List[ActivityCandidate]:
        """
        Uses Neural Search to find 5-10 real-world candidates 
        based on the structured Vibe.
        """
        # Construct a 'Neural-friendly' string
        # Exa works best when you describe the result you want to find.
        search_query = f"The best {vibe.environment_pref} {vibe.energy_level} energy spots in {location} for {', '.join(vibe.tags)}"
        
        # 1. Perform the Neural Search
        # 'use_autoprompt' lets Exa optimize your query for AI
        results = self.exa.search(
            search_query,
            num_results=8,
        )

        # 2. Map Exa results to your ActivityCandidate schema
        candidates = []
        for res in results.results:
            candidates.append(ActivityCandidate(
                name=res.title,
                description=res.summary if hasattr(res, 'summary') and res.summary else res.title,
                url=res.url,
                location_name=location,
                score=res.score or 0.0,
                category="activity"
            ))
            
        return candidates
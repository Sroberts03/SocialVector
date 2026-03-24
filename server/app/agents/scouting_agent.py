from exa_py import Exa
from typing import List
from app.models.schemas import ActivityCandidate, LocationInfo, VibeSchema
from datetime import datetime
from app.prompts.agent_prompts import SEARCH_QUERY

class ScoutingAgent:
    def __init__(self, exa_client: Exa):
        # We pass the client initialized in agents.py (the singleton)
        self.exa = exa_client

    async def run(self, vibe: VibeSchema, location_info: LocationInfo ) -> List[ActivityCandidate]:
        """
        Uses Neural Search to find 5-10 real-world candidates 
        based on the structured Vibe.
        """
        # Construct a 'Neural-friendly' string
        # Exa works best when you describe the result you want to find.
        
        # 1. Perform the Neural Search
        results = self.exa.search(
            SEARCH_QUERY.format(
                environment_pref=vibe.environment_pref,
                energy_level=vibe.energy_level,
                time_for_activity=vibe.time_for_activity,
                formatted_address=location_info.formatted_address,
                tags=", ".join(vibe.tags)
            ),
            num_results=10,
        )

        # 2. Map Exa results to your ActivityCandidate schema
        candidates = []
        for res in results.results:
            candidates.append(ActivityCandidate(
                name=res.title,
                description=res.summary if hasattr(res, 'summary') and res.summary else res.title,
                url=res.url,
                location_name=location_info.formatted_address,
                score=res.score or 0.0,
                category="activity"
            ))
            
        return candidates
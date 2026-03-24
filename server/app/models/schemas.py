from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union

class VibeSchema(BaseModel):
    """The output of the Vibe Agent. Influences all following agents."""
    energy_level: Literal["Low", "Medium", "High"]
    social_intent: Literal["Solo", "Small Group", "Large Crowd"]
    environment_pref: Literal["Indoor", "Outdoor", "Any"]
    tags: List[str] = Field(description="Keywords for Exa search, e.g. ['basketball', 'hiking']")
    reasoning: str = Field(description="Remy's internal thought process for this vibe")
    time_for_activity: Literal["Morning", "Afternoon", "Evening"]

class ActivityCandidate(BaseModel):
    """A raw activity found by the Scout Agent."""
    name: str
    description: str
    location_name: str
    url: str
    category: str

class FinalActivity(ActivityCandidate):
    """The verified activity chosen by the Choice and Reviewer Agents."""
    lat: float
    lon: float
    start_time: str
    weather_ok: bool
    review_status: str = Field(description="Comment from the Reviewer Agent")

class FinalReview(FinalActivity):
    """The final output of the Reviewer Agent."""
    status: Literal["PASS", "REJECT"]
    reason: Optional[str] = Field(description="If REJECT, explain why.")
    adjustment: Optional[str] = Field(description="If REJECT, suggest a modification to make it PASS.")

class LocationInfo(BaseModel):
    city: str
    state: str
    formatted_address: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    is_precise: bool = Field(description="True if we have a precise location, False if it's a fallback based on IP or user context")

class WeatherInfo(BaseModel):
    temp: Union[float, str]
    condition: str
    description: str
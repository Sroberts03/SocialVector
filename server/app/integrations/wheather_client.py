import httpx
import os

class WheatherClient:
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url

    async def get_weather(self, city: str = "Rexburg"):
        """Fetches current weather to see if outdoor activities are safe."""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temp": data["main"]["temp"],
                    "condition": data["weather"][0]["main"],
                    "description": data["weather"][0]["description"]
                }
            return None
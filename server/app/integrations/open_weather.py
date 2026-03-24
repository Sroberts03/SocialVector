import httpx

class OpenWeather:
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather(self, formatted_address: str = None, lat: float = None, lon: float = None) -> dict:
        """Fetches current weather to see if outdoor activities are safe."""
        params = {
            "appid": self.api_key,
            "units": "imperial"
        }
        
        # Prefer coordinates over city name (more reliable)
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
            print(f"Fetching weather by coordinates: lat={lat}, lon={lon}")
        elif formatted_address:
            params["q"] = formatted_address
            print(f"Fetching weather by address: {formatted_address}")
        else:
            raise ValueError("Must provide either coordinates or formatted_address")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temp": data["main"]["temp"],
                        "condition": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"]
                    }
                else:
                    print(f"Failed to fetch weather data: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"Exception during weather fetch: {type(e).__name__}: {e}")
            return None
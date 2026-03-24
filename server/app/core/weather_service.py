from app.integrations.open_weather import OpenWeather
from app.models.schemas import LocationInfo, WeatherInfo

class WeatherService:
    def __init__(self, weather_client: OpenWeather):
        self.open_weather = weather_client
    
    async def get_weather(self, location: LocationInfo) -> WeatherInfo:
        print(f"Fetching weather for location: {location.formatted_address}")
        
        # Try coordinates first, fall back to address
        weather_data = await self.open_weather.get_weather(
            lat=location.lat,
            lon=location.lon,
            formatted_address=location.formatted_address
        )
        
        if not weather_data:
            print("Weather data is unavailable, returning default values.")
            return WeatherInfo(temp="unknown", condition="unknown", description="unknown conditions")
        
        temp = weather_data.get("temp", "unknown")
        condition = weather_data.get("condition", "unknown")
        description = weather_data.get("description", "unknown conditions")
        
        print(f"Weather data for {location.formatted_address}: Temp={temp}, Condition={condition}, Description={description}")
        return WeatherInfo(temp=temp, condition=condition, description=description)
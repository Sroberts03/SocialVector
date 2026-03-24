from app.models.schemas import LocationInfo


class Location:
    def __init__(self, google_maps_client=None):
        self.google_maps_client = google_maps_client
        self.cache = {}

    async def get_location_info(self, user_context: dict, latitude: float = None, longitude: float = None) -> LocationInfo:
        if self.google_maps_client and latitude is not None and longitude is not None:
            key = f"{latitude},{longitude}"
            if key in self.cache:
                return self.cache[key]
            try:
                location_info = await self.google_maps_client.get_location_info(latitude, longitude)
            except Exception as e:
                print(f"Error getting location info: {e}")
                location_info = None
            if location_info:
                normalized = self.normalize_location(location_info, latitude, longitude)
                self.cache[key] = normalized
                return normalized
        # Fallback to user context or default
        print("Falling back to user context for location info.")
        return LocationInfo(
            city=user_context.get("city") or "Unknown City",
            state=user_context.get("state") or "Unknown State",
            formatted_address=f"{user_context.get('city', '')}, {user_context.get('state', '')}".strip(", "),
            lat=user_context.get("lat") if user_context.get("lat") else None,
            lon=user_context.get("lon") if user_context.get("lon") else None,
            is_precise=False
        )

    def normalize_location(self, location_info: dict, lat: float, lon: float) -> LocationInfo:
        components = location_info.get("address_components", [])
        city, state, country = None, None, None
        for comp in components:
            types = comp["types"]
            if "locality" in types or  "sublocality" in types or "postal_town" in types:
                city = comp["long_name"]
            elif "administrative_area_level_1" in types:
                state = comp["short_name"]
            elif "country" in types:
                country = comp["long_name"]
        if city and state:
            return LocationInfo(city=city, state=state, formatted_address=city + ", " + state, lat=lat, lon=lon, is_precise=True)
        
        return LocationInfo(city=None, state=None, formatted_address=None, lat=None, lon=None, is_precise=False)
            
            
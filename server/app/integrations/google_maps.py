import aiohttp

class GoogleMapsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def get_location_info(self, latitude, longitude):
        url = "https://maps.googleapis.com/maps/api/geocode/json"

        params = {
            "latlng": f"{latitude},{longitude}",
            "key": self.api_key
        }

        session = await self._get_session()

        async with await session.get(url, params=params) as response:
            if response.status != 200:
                return None

            data = await response.json()

            if data["status"] == "OK" and data["results"]:
                return data["results"][0]

            return None
        
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
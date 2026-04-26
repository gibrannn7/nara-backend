import httpx
import base64
import json
from app.core.config import settings
from app.core.logger import log
from app.core.utils import async_retry

class MixpanelAdapter:
    def __init__(self):
        self.token = settings.MIXPANEL_TOKEN
        self.base_url = "https://api.mixpanel.com/track"

    @async_retry(retries=3, delay=1.0)
    async def track_event(self, user_id: str, event_name: str, properties: dict = None) -> bool:
        if properties is None:
            properties = {}
        
        properties.update({
            "token": self.token,
            "distinct_id": user_id
        })
        
        payload = {
            "event": event_name,
            "properties": properties
        }
        
        # Mixpanel API expects base64 encoded data parameter for GET/POST
        encoded_data = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                data={"data": encoded_data},
                headers={"Accept": "text/plain"}
            )
            
            response.raise_for_status()
            log.info(f"Mixpanel event '{event_name}' tracked for user {user_id}")
            return True
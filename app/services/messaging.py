import httpx
from typing import List
from app.core.config import settings
from app.core.logger import log
from app.core.utils import async_retry

class OneSignalAdapter:
    def __init__(self):
        self.app_id = settings.ONESIGNAL_APP_ID
        self.api_key = settings.ONESIGNAL_API_KEY
        self.base_url = "https://onesignal.com/api/v1/notifications"

    @async_retry(retries=2, delay=2.0)
    async def send_notification(self, heading: str, content: str, target_user_ids: List[str]) -> dict:
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "app_id": self.app_id,
            "include_external_user_ids": target_user_ids,
            "headings": {"en": heading},
            "contents": {"en": content}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            log.info(f"OneSignal notification sent successfully. Response: {result}")
            return result
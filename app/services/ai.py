import httpx
from app.core.config import settings
from app.core.logger import log
from app.core.utils import async_retry

class GroqAdapter:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    @async_retry(retries=2, delay=1.5)
    async def optimize_campaign_content(self, raw_content: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "You are an expert marketing copywriter. "
            "Optimize the provided text to be highly engaging and conversion-focused. "
            "Return only the optimized text, no explanations."
        )
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_content}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=15.0
            )
            response.raise_for_status()
            result = response.json()
            optimized_text = result["choices"][0]["message"]["content"].strip()
            log.info("Groq successfully optimized campaign content.")
            return optimized_text
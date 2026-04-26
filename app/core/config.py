from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GCP_LOCATION: str
    GCP_QUEUE_NAME: str

    MIXPANEL_TOKEN: str
    MIXPANEL_API_SECRET: str
    ONESIGNAL_APP_ID: str
    ONESIGNAL_API_KEY: str
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Hanya set env var jika filenya benar-benar ada (untuk lokal)
import os
if settings.GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(settings.GOOGLE_APPLICATION_CREDENTIALS):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
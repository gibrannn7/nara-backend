import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # GCP Config
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GCP_LOCATION: str
    GCP_QUEUE_NAME: str

    # Mixpanel
    MIXPANEL_TOKEN: str
    MIXPANEL_API_SECRET: str

    # OneSignal
    ONESIGNAL_APP_ID: str
    ONESIGNAL_API_KEY: str

    # Groq
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# FIX: Menyuntikkan kredensial ke OS Environment agar terdeteksi oleh GCP SDK
if settings.GOOGLE_APPLICATION_CREDENTIALS:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
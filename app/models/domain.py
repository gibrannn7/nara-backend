from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class UserDTO(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: str = Field(default_factory=utc_now)

class CampaignDTO(BaseModel):
    id: str
    owner_id: str
    title: str
    content: str
    status: str = Field(default="draft")  # draft, queued, sent, failed
    ai_metadata: Optional[Dict[str, Any]] = None
    created_at: str = Field(default_factory=utc_now)
    scheduled_at: Optional[str] = None
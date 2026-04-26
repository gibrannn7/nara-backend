from pydantic import BaseModel, Field
from typing import Optional

class CampaignCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    raw_content: str = Field(..., min_length=10)
    scheduled_at: Optional[str] = None
    optimize_with_ai: bool = Field(default=False)

class CampaignResponse(BaseModel):
    id: str
    title: str
    content: str
    status: str
    created_at: str
    
    class Config:
        from_attributes = True
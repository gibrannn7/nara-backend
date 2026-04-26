from fastapi import APIRouter, Depends, HTTPException, status
from app.api.auth import verify_api_key
from app.models.dtos import CampaignCreateRequest, CampaignResponse
from app.models.domain import CampaignDTO
from app.db.firestore import db_instance
from app.repositories.base import BaseRepository
from app.services.campaign_service import CampaignService
from app.services.ai import GroqAdapter
from app.services.task_dispatcher import CloudTasksDispatcher
from app.services.analytics import MixpanelAdapter

router = APIRouter(prefix="/v1/campaigns", tags=["Campaigns"])

# Dependency Injection Builder
def get_campaign_service() -> CampaignService:
    # Ideally, use a robust DI container (like python-dependency-injector)
    # For this scale, functional injection is sufficient and explicit
    repo = BaseRepository(db_instance.client, CampaignDTO, "campaigns")
    return CampaignService(
        campaign_repo=repo,
        ai_adapter=GroqAdapter(),
        task_dispatcher=CloudTasksDispatcher(base_worker_url="http://localhost:8000"),
        analytics_adapter=MixpanelAdapter()
    )

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    request: CampaignCreateRequest,
    current_user_id: str = Depends(verify_api_key),
    service: CampaignService = Depends(get_campaign_service)
):
    try:
        campaign = await service.create_campaign(
            owner_id=current_user_id,
            title=request.title,
            raw_content=request.raw_content,
            optimize=request.optimize_with_ai
        )
        return campaign
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
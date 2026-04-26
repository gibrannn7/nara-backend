import uuid
from app.repositories.base import BaseRepository
from app.models.domain import CampaignDTO
from app.services.ai import GroqAdapter
from app.services.task_dispatcher import CloudTasksDispatcher
from app.services.analytics import MixpanelAdapter
from app.core.logger import log

class CampaignService:
    def __init__(
        self, 
        campaign_repo: BaseRepository[CampaignDTO],
        ai_adapter: GroqAdapter,
        task_dispatcher: CloudTasksDispatcher,
        analytics_adapter: MixpanelAdapter
    ):
        self.repo = campaign_repo
        self.ai = ai_adapter
        self.dispatcher = task_dispatcher
        self.analytics = analytics_adapter

    async def create_campaign(self, owner_id: str, title: str, raw_content: str, optimize: bool) -> CampaignDTO:
        final_content = raw_content
        ai_meta = None

        if optimize:
            log.info(f"Optimizing content for campaign: {title}")
            final_content = await self.ai.optimize_campaign_content(raw_content)
            ai_meta = {"optimized": True, "model": self.ai.model}

        campaign_id = f"camp_{uuid.uuid4().hex[:12]}"
        new_campaign = CampaignDTO(
            id=campaign_id,
            owner_id=owner_id,
            title=title,
            content=final_content,
            ai_metadata=ai_meta,
            status="queued"
        )

        # 1. Save to Database
        saved_campaign = await self.repo.create(campaign_id, new_campaign)
        
        # 2. Dispatch to Cloud Tasks (Async Worker)
        self.dispatcher.enqueue_campaign_task(campaign_id, owner_id)

        # 3. Track Analytics (Fire and forget, handled by adapter)
        await self.analytics.track_event(
            user_id=owner_id,
            event_name="campaign_created",
            properties={"campaign_id": campaign_id, "ai_used": optimize}
        )

        return saved_campaign
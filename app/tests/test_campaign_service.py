import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.campaign_service import CampaignService
from app.models.domain import CampaignDTO

@pytest.mark.asyncio
async def test_create_campaign_with_ai_optimization():
    # Arrange: Mock dependencies
    mock_repo = AsyncMock()
    mock_repo.create.return_value = CampaignDTO(
        id="test_123",
        owner_id="user_1",
        title="Test",
        content="Optimized content",
        status="queued"
    )
    
    mock_ai = AsyncMock()
    mock_ai.optimize_campaign_content.return_value = "Optimized content"
    
    mock_dispatcher = MagicMock()
    mock_analytics = AsyncMock()

    service = CampaignService(mock_repo, mock_ai, mock_dispatcher, mock_analytics)

    # Act
    result = await service.create_campaign(
        owner_id="user_1",
        title="Test Promo",
        raw_content="Buy now",
        optimize=True
    )

    # Assert
    assert result.content == "Optimized content"
    mock_ai.optimize_campaign_content.assert_called_once_with("Buy now")
    mock_dispatcher.enqueue_campaign_task.assert_called_once()
    mock_analytics.track_event.assert_called_once()
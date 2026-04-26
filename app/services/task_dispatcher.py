import json
from google.cloud import tasks_v2
from app.core.config import settings
from app.core.logger import log
from app.core.exceptions import InfrastructureException

class CloudTasksDispatcher:
    def __init__(self, base_worker_url: str):
        # Dalam production, base_worker_url adalah URL Cloud Run Anda
        # Untuk lokal, gunakan ngrok URL atau host docker Anda
        self.base_worker_url = base_worker_url
        self.project = settings.GOOGLE_CLOUD_PROJECT
        self.location = settings.GCP_LOCATION
        self.queue = settings.GCP_QUEUE_NAME
        
        try:
            self.client = tasks_v2.CloudTasksClient()
            self.parent = self.client.queue_path(self.project, self.location, self.queue)
        except Exception as e:
            log.error(f"Failed to initialize Cloud Tasks Client: {str(e)}")
            raise InfrastructureException("Cloud Tasks initialization failed.")

    def enqueue_campaign_task(self, campaign_id: str, owner_id: str) -> bool:
        task_payload = {
            "campaign_id": campaign_id,
            "owner_id": owner_id
        }
        
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": f"{self.base_worker_url}/api/v1/internal/tasks/process-campaign",
                "headers": {"Content-type": "application/json"},
                "body": json.dumps(task_payload).encode()
            }
        }

        try:
            response = self.client.create_task(
                request={"parent": self.parent, "task": task}
            )
            log.info(f"Task created for campaign {campaign_id}: {response.name}")
            return True
        except Exception as e:
            log.error(f"Failed to enqueue task for campaign {campaign_id}: {str(e)}")
            raise InfrastructureException("Failed to dispatch task to GCP.")
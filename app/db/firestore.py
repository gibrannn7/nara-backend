from google.cloud import firestore
from app.core.config import settings
from app.core.logger import log
from app.core.exceptions import InfrastructureException

class FirestoreDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(FirestoreDB, cls).__new__(cls)
                cls._instance.client = firestore.AsyncClient(
                    project=settings.GOOGLE_CLOUD_PROJECT,
                    database="nara"
                )
                log.info("Firestore AsyncClient connected to 'nara' database.")
            except Exception as e:
                log.error(f"Failed to initialize Firestore: {str(e)}")
                raise InfrastructureException(f"Database connection failed: {str(e)}")
        return cls._instance

# Singleton instance
db_instance = FirestoreDB()
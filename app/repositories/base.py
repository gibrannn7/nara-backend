from typing import TypeVar, Generic, Type, Optional, List
from google.cloud.firestore import AsyncClient
from pydantic import BaseModel
from app.core.logger import log
from app.core.exceptions import ResourceNotFoundException, InfrastructureException

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncClient, model_class: Type[T], collection_name: str):
        self.db = db
        self.model_class = model_class
        self.collection = self.db.collection(collection_name)

    async def get_by_id(self, doc_id: str) -> Optional[T]:
        try:
            doc_ref = self.collection.document(doc_id)
            doc = await doc_ref.get()
            if not doc.exists:
                return None
            
            data = doc.to_dict()
            data['id'] = doc.id
            return self.model_class(**data)
        except Exception as e:
            log.error(f"Error fetching {doc_id} from {self.collection.id}: {str(e)}")
            raise InfrastructureException(f"Database read error: {str(e)}")

    async def create(self, doc_id: str, data: T) -> T:
        try:
            doc_ref = self.collection.document(doc_id)
            data_dict = data.model_dump(exclude={"id"})
            await doc_ref.set(data_dict)
            return data
        except Exception as e:
            log.error(f"Error creating document in {self.collection.id}: {str(e)}")
            raise InfrastructureException(f"Database write error: {str(e)}")
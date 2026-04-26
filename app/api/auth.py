from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    # In a real-world scenario, this should query a Database or Redis
    # For this portfolio, we use a static admin key from .env
    valid_key = getattr(settings, "NARA_ADMIN_API_KEY", "default_dev_key_123")
    
    if not api_key or api_key != valid_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return "admin_user_id"
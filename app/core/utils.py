import asyncio
from functools import wraps
from typing import Callable, Any
from app.core.logger import log
from app.core.exceptions import InfrastructureException

def async_retry(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        log.error(f"Function {func.__name__} failed after {retries} attempts. Error: {str(e)}")
                        raise InfrastructureException(f"External service failure: {str(e)}")
                    log.warning(f"Function {func.__name__} attempt {attempt} failed. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
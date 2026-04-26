from fastapi import FastAPI
from app.core.logger import log
from app.api.routes import campaigns
# from app.api.routes import tasks # Assuming tasks router from Phase 4 is registered here

app = FastAPI(
    title="Nara Campaign API",
    description="Backend engine for AI-backed notifications and analytics",
    version="1.0.0"
)

app.include_router(campaigns.router)

@app.on_event("startup")
async def startup_event():
    log.info("Nara Backend API is starting up...")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
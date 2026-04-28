from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.hotspots import router as hotspots_router
from app.api.routes.review_tasks import router as review_tasks_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(hotspots_router, prefix="/hotspots", tags=["hotspots"])
api_router.include_router(review_tasks_router, prefix="/review-tasks", tags=["review-tasks"])

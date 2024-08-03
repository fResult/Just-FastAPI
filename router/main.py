from fastapi import APIRouter

from .test_route import router as test_router

routers = APIRouter()

routers.include_router(test_router)

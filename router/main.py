from fastapi import APIRouter

from .cqrs_route import router as cqrs_router
from .test_route import router as test_router

routers = APIRouter()

routers.include_router(test_router)
routers.include_router(cqrs_router)

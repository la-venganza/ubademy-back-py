from fastapi import APIRouter

from app.api.api_v1.resources import courses, users


api_router = APIRouter()
api_router.include_router(courses.router_v1, prefix="/courses", tags=["courses"])
api_router.include_router(users.router_v1, prefix="/users", tags=["users"])

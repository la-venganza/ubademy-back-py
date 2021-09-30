from fastapi import APIRouter

from app.courses.api_v1 import resources


course_router = APIRouter()
course_router.include_router(resources.router_v1, prefix="/courses", tags=["courses"])

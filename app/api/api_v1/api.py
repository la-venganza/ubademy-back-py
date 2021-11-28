from fastapi import APIRouter

from app.api.api_v1.resources import courses, users, exams, subscriptions


api_router = APIRouter()
api_router.include_router(courses.router_v1, prefix="/courses", tags=["courses"])
api_router.include_router(exams.router_v1, prefix="/courses/{course_id}/lessons/{lesson_id}/exams", tags=["exam"])
api_router.include_router(users.router_v1, prefix="/users", tags=["users"])
api_router.include_router(subscriptions.router_v1, prefix="/{user_id}/subscriptions", tags=["subscriptions"])

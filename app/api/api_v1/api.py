from fastapi import APIRouter

from app.api.api_v1.resources import courses, users, exams, subscriptions, courses_exams, subscription_plans,\
    enroll_courses


api_router = APIRouter()
api_router.include_router(courses.router_v1, prefix="/courses", tags=["courses"])
api_router.include_router(exams.router_v1, prefix="/courses/{course_id}/lessons/{lesson_id}/exams", tags=["exams"])
api_router.include_router(users.router_v1, prefix="/users", tags=["users"])
api_router.include_router(subscriptions.router_v1, prefix="/{user_id}/subscriptions", tags=["subscriptions"])
api_router.include_router(courses_exams.router_v1, prefix="/courses", tags=["exams"])
api_router.include_router(subscription_plans.router_v1, prefix="/subscription_plans", tags=["subscription_plans"])
api_router.include_router(enroll_courses.router_v1, prefix="/courses/{course_id}/registration", tags=["enrollments"])

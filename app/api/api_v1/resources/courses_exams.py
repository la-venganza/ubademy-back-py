import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from app import deps
from app.schemas.course_exam import CourseExamResults
from app.services import course_service

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=status.HTTP_200_OK, response_model=CourseExamResults)
async def search_exams(
    *,
    user_id: str = Query(None, example="someUserId"),
    active_students: Optional[bool] = Query(None, example="false"),
    graded_status: Optional[bool] = Query(None, example="false"),
    page_size: Optional[int] = 10,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for exams taken by students, relevant for course creators/collaborators.
    """
    await pagination_validator(page=page, page_size=page_size)

    course_exams = await course_service.get_exams_for_staff(
        db=db, staff_id=user_id, active_students_filter=active_students,
        graded_status_filter=graded_status, pagination_limit=page_size,
        pagination_offset=(page - 1) * page_size)
    return {"results": course_exams}


async def pagination_validator(page, page_size):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page value must be at least 1")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page size must be at least 1")

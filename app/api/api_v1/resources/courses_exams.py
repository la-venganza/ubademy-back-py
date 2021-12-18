import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import deps
from app.schemas.course_exam import CourseExamResults, ExamResults
from app.services import course_service
from app.utils import pagination_utils

logger = logging.getLogger(__name__)

course_exams_suffix = "/lessons/exams"
router_v1 = APIRouter()


@router_v1.get(course_exams_suffix, status_code=status.HTTP_200_OK, response_model=CourseExamResults)
async def search_staff_to_grade_exams(
    *,
    user_id: str = Query(..., example="someUserId"),
    active_students: Optional[bool] = Query(None, example="false"),
    graded_status: Optional[bool] = Query(None, example="false"),
    page_size: Optional[int] = 10,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for exams taken by students, relevant for course creators/collaborators.
    """
    await pagination_utils.validate_pagination(page=page, page_size=page_size)

    course_exams = await course_service.get_exams_for_staff(
        db=db, staff_id=user_id, active_students_filter=active_students,
        graded_status_filter=graded_status, pagination_limit=page_size,
        pagination_offset=(page - 1) * page_size)
    return {"results": course_exams}


@router_v1.get("/{course_id}" + course_exams_suffix, status_code=status.HTTP_200_OK, response_model=ExamResults)
async def search_course_exams(
    *,
    course_id: int,
    user_id: str = Query(..., example="someUserId"),
    page_size: Optional[int] = 10,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    List exams basic info from a course, relevant for course creator/collaborators.
    """
    await pagination_utils.validate_pagination(page=page, page_size=page_size)

    course_exams = await course_service.get_course_exams_for_staff(
        db=db, staff_id=user_id, course_id=course_id, pagination_limit=page_size, pagination_offset=(page - 1) * page_size)
    return {"results": course_exams}

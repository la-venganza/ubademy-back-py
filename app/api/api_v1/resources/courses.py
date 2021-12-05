import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from app.services import course_service, user_service
from app.schemas.course.course import CourseCreate, Course, CourseSearchResults, \
    CourseRegistration, CourseCollaboration, CourseUpdateRq
from app import deps, crud
from app.models.enroll_course import EnrollCourse as EnrollCourseDb
from app.schemas.enroll_course import EnrollCourse
from app.models.collaborator import Collaborator as CollaboratorDb
from app.schemas.collaborator import Collaborator

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=status.HTTP_200_OK, response_model=CourseSearchResults)
async def search_courses(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="java"),
    max_results: Optional[int] = 10,
    page_size: Optional[int] = 10,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for courses based on hashtags keyword
    """
    await pagination_validator(page=page, page_size=page_size)
    courses = crud.course.get_multi(db=db, limit=page_size, offset=(page - 1) * page_size)
    if not keyword:
        return {"results": courses}

    results = filter(lambda course: keyword.lower() in course.hashtags.lower(), courses)
    return {"results": list(results)[:max_results]}


@router_v1.post("/", status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course_in: CourseCreate, db: Session = Depends(deps.get_db),) -> dict:
    user_id = course_in.creator_id
    await user_service.get_user_by_id(db=db, user_id=user_id)

    course = crud.course.create(db=db, obj_in=course_in)

    return course


@router_v1.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=Course)
async def get(course_id: int, db: Session = Depends(deps.get_db), ):
    """
    Get a single course by id
    """
    logging.info(f"Getting course id {course_id}")
    course = crud.course.get_full_by_course_id(db=db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The course with id {course_id} was not found")

    return course


@router_v1.post("/{course_id}/registration", status_code=status.HTTP_200_OK, response_model=EnrollCourse)
async def course_registration(course_id: int, course_registration_rq: CourseRegistration,
                              db: Session = Depends(deps.get_db),) -> dict:
    """
    Register a user in a course as a student
    """
    course = await course_service.get_course_by_id(course_id, db)

    user_id = course_registration_rq.user_id
    user = await user_service.get_user_by_id(db=db, user_id=user_id)

    if any(filter(lambda enroll_course: str(course_id) in str(enroll_course.course_id), user.enroll_courses)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_id} is already register in course {course_id}")

    student_enroll_course = crud.enroll_course.create(db=db, obj_in=EnrollCourseDb(user_id=user_id, course_id=course.id))

    return student_enroll_course


@router_v1.post("/{course_id}/collaboration", status_code=status.HTTP_200_OK, response_model=Collaborator)
async def course_collaboration(course_id: int, course_collaboration_rq: CourseCollaboration,
                               db: Session = Depends(deps.get_db),) -> dict:
    """
    Register a user in a course as a collaborator
    """
    user_id = course_collaboration_rq.user_id
    await course_service.verify_course_with_creator(course_id=course_id, user_id=user_id, db=db)

    collaborator_id = course_collaboration_rq.collaborator_id
    user = await user_service.get_user_by_id(db=db, user_id=collaborator_id)

    if any(filter(lambda course: str(course_id) in str(course.id), user.collaborating_courses)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {collaborator_id} is already collaborating in course {course_id}")

    collaborator_enrollment = crud.collaborator.create(
        db=db, obj_in=CollaboratorDb(user_id=collaborator_id, course_id=course_id)
    )

    return collaborator_enrollment


@router_v1.patch("/{course_id}", status_code=status.HTTP_200_OK, response_model=Course)
async def update_course(course_id: int, course_update_rq: CourseUpdateRq,
                        db: Session = Depends(deps.get_db), ) -> dict:
    """
    Update a course by its creator
    """
    user_id = course_update_rq.user_id
    await user_service.get_user_by_id(db=db, user_id=user_id)

    course = await course_service.get_course_by_id(course_id=course_id, db=db)

    if course.creator_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id {user_id} is not the creator of course with id {course_id}"
        )

    course_updated = crud.course.patch_course(
        db=db,
        course_to_update=course_update_rq.course,
        course_db_data=course
    )

    return course_updated


async def pagination_validator(page, page_size):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page value must be at least 1")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Page size must be at least 1")

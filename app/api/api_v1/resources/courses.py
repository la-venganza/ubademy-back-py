import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.course.course import CourseCreate, Course, CourseSearchResults, CourseRegistration, CourseCollaboration
from app import deps
from app import crud
# from common.error_handling import ObjectNotFound

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/search/", status_code=status.HTTP_200_OK, response_model=CourseSearchResults)
async def search_courses(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="java"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for courses based on hashtags keyword
    """
    courses = crud.course.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": courses}

    results = filter(lambda course: keyword.lower() in course.hashtags.lower(), courses)
    return {"results": list(results)[:max_results]}


@router_v1.post("/", status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course_in: CourseCreate, db: Session = Depends(deps.get_db),) -> dict:
    user_id = course_in.creator_id
    user = crud.user.get_by_user_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")

    course = crud.course.create(db=db, obj_in=course_in)

    return course


@router_v1.get("/{course_id}", status_code=status.HTTP_200_OK)
async def get(course_id: int, db: Session = Depends(deps.get_db), ):
    """
    Get a single course by id
    """
    logging.info(f"Getting course id {course_id}")
    course = crud.course.get_full_by_course_id(db=db, course_id=course_id)
    if course is None:
        # raise ObjectNotFound('The course doesnt not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The course with id {course_id} was not found")

    return course


@router_v1.post("/{course_id}/registration", status_code=status.HTTP_200_OK, response_model=Course)
async def course_registration(course_id: int, course_registration_rq: CourseRegistration,
                              db: Session = Depends(deps.get_db),) -> dict:
    course = crud.course.get(db=db, id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {course_id} was not found")

    user_id = course_registration_rq.user_id
    user = crud.user.get_by_user_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")

    if any(filter(lambda course: str(course_id) in str(course.id), user.attending_courses)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_id} is already register in course {course_id}")

    user.attending_courses.append(course)

    crud.user.update_user(db=db, updated_user=user)

    return course


@router_v1.post("/{course_id}/collaboration", status_code=status.HTTP_200_OK, response_model=Course)
async def course_registration(course_id: int, course_collaboration_rq: CourseCollaboration,
                              db: Session = Depends(deps.get_db),) -> dict:
    course = crud.course.get(db=db, id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Course with id {course_id} was not found")

    user_id = course_collaboration_rq.user_id
    user = crud.user.get_by_user_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")

    if any(filter(lambda course: str(course_id) in str(course.id), user.collaborating_courses)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_id} is already register in course {course_id}")

    user.collaborating_courses.append(course)

    crud.user.update_user(db=db, updated_user=user)

    return course

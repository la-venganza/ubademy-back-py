import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from app.services import course_service, user_service
from app.schemas.course.course import CourseCreate, CourseCreateRQ, Course, CourseSearchResults, \
    CourseCollaboration, CourseUpdateRq, CourseType, CourseTypeResults, CourseStudent, CourseCollaborator, \
    CourseCreator, CourseBasics, CourseGlobal
from app import deps, crud
from app.models.collaborator import Collaborator as CollaboratorDb
from app.schemas.collaborator import Collaborator
from app.services import subscription_service
from app.schemas.subscription import SubscriptionTitle
from app.utils import pagination_utils

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/types", status_code=status.HTTP_200_OK, response_model=CourseTypeResults)
async def get_course_types():
    """
    Get values of course types allowed for courses
    """
    logging.info(f"Getting course types list")
    return {"course_types": CourseType.list()}


@router_v1.get("", status_code=status.HTTP_200_OK, response_model=CourseSearchResults)
async def search_courses(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="java"),
        category: Optional[CourseType] = Query(None, example=CourseType.programming),
        plan: Optional[SubscriptionTitle] = Query(None, example=SubscriptionTitle.free),
        max_results: Optional[int] = 10,
        page_size: Optional[int] = 10,
        page: Optional[int] = 1,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for courses based on hashtags keyword
    Max results param is only taken into account when keyword param is sent
    """
    await pagination_utils.validate_pagination(page=page, page_size=page_size)
    courses = crud.course.get_courses_with_filters(db=db, category_filter=category, plan_filter=plan,
                                                   limit=page_size, offset=(page - 1) * page_size)
    if not keyword:
        return {"results": courses}

    results = filter(lambda course: keyword.lower() in course.hashtags.lower(), courses)
    return {"results": list(results)[:max_results]}


@router_v1.post("", status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course_in: CourseCreateRQ, db: Session = Depends(deps.get_db), ) -> dict:
    user_id = course_in.user_id
    await user_service.get_user_by_id(db=db, user_id=user_id)

    subscription_required = await subscription_service.get_subscription_by_subscription_plan(
        subscription_plan_in=course_in.subscription_required, db=db
    )

    course = crud.course.create(db=db,
                                obj_in=CourseCreate(
                                    title=course_in.title,
                                    description=course_in.description,
                                    type=course_in.type,
                                    hashtags=course_in.hashtags,
                                    location=course_in.location,
                                    lessons=course_in.lessons,
                                    creator_id=course_in.user_id,
                                    subscription_id_required=subscription_required.id)
                                )
    return course


@router_v1.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=Union[CourseGlobal, Course])
async def get(
        course_id: int,
        user_id: Optional[str] = Query(None, example="userId"),
        db: Session = Depends(deps.get_db), ):
    """
    Get a single course by id
    """
    logging.info(f"Getting course id {course_id}")
    course = crud.course.get(db=db, id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The course with id {course_id} was not found")
    if user_id:
        if any(enrollment.user_id == user_id and enrollment.active for enrollment in course.enrollments):
            return CourseStudent.from_orm(course)
        elif any(collaborator.user_id == user_id and collaborator.active for collaborator in course.collaborators):
            return CourseCollaborator.from_orm(course)
        elif course.creator_id == user_id:
            return CourseCreator.from_orm(course)
        else:
            return CourseBasics.from_orm(course)

    return Course.from_orm(course)


@router_v1.post("/{course_id}/collaboration", status_code=status.HTTP_200_OK, response_model=Collaborator)
async def course_collaboration(course_id: int, course_collaboration_rq: CourseCollaboration,
                               db: Session = Depends(deps.get_db), ) -> dict:
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

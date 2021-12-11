import logging

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.services import course_service, user_service
from app.schemas.course.course import CourseRegistration
from app import deps, crud
from app.models.enroll_course import EnrollCourse as EnrollCourseDb
from app.schemas.enroll_course import EnrollCourse, EnrollCourseUpdate
from app.services import subscription_service
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionTitle

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


def validate_user_subscription_against_course_subscription(user_subscription: Subscription,
                                                           course_subscription_required: Subscription):
    if course_subscription_required.title.lower() == SubscriptionTitle.free.lower():
        return True
    elif course_subscription_required.title.lower() == SubscriptionTitle.gold.lower():
        return True if (user_subscription.title.lower() == SubscriptionTitle.gold.lower()
                        or user_subscription.title.lower() == SubscriptionTitle.premium.lower()) else False
    elif course_subscription_required.title.lower() == SubscriptionTitle.premium.lower():
        return True if user_subscription.title.lower() == SubscriptionTitle.premium.lower() else False


@router_v1.post("", status_code=status.HTTP_200_OK, response_model=EnrollCourse)
async def course_registration(course_id: int, course_registration_rq: CourseRegistration,
                              db: Session = Depends(deps.get_db), ) -> dict:
    """
    Register a user in a course as a student
    """
    course = await course_service.get_course_by_id(course_id, db)

    user_id = course_registration_rq.user_id
    user = await user_service.get_user_by_id(db=db, user_id=user_id)

    student_enrollment = next(
        filter(lambda enroll_course: course_id == enroll_course.course_id, user.enroll_courses), None)
    if student_enrollment and student_enrollment.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_id} is already register in course {course_id}")

    user_current_subscription = subscription_service.get_current_subscription(user.subscriptions)
    subscription_validated = validate_user_subscription_against_course_subscription(
        user_subscription=user_current_subscription.subscription,
        course_subscription_required=course.subscription_required
    )
    if not subscription_validated:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The course with id {course_id} requires a {course.subscription_required.title} subscription and"
                   f" user {user_id} has a {user_current_subscription.subscription.title} subscription")

    if student_enrollment:
        student_enroll_course_response = crud.enroll_course.update(
            db=db, db_obj=student_enrollment, obj_in=EnrollCourseUpdate(active=True))
    else:
        student_enroll_course_response = crud.enroll_course.create(
            db=db, obj_in=EnrollCourseDb(user_id=user_id, course_id=course.id))

    return student_enroll_course_response


@router_v1.patch("", status_code=status.HTTP_200_OK, response_model=EnrollCourse)
async def course_unregister(course_id: int, course_registration_rq: CourseRegistration,
                            db: Session = Depends(deps.get_db), ) -> dict:
    """
    Unregister a user from a course
    """
    await course_service.get_course_by_id(course_id, db)

    user_id = course_registration_rq.user_id
    user = await user_service.get_user_by_id(db=db, user_id=user_id)

    student_enroll_course = next(filter(lambda enroll_course:
                                        course_id == enroll_course.course_id
                                        and enroll_course.active, user.enroll_courses)
                                 , None)

    if student_enroll_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} is not register in course {course_id}")

    student_disenroll_course = crud.enroll_course.update(
        db=db, db_obj=student_enroll_course, obj_in=EnrollCourseUpdate(active=False)
    )

    return student_disenroll_course

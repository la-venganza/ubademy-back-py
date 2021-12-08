from unittest.mock import MagicMock

from app.crud import course
from app.schemas.course.course import CourseUpdate, CourseType
from app.schemas.subscription import SubscriptionTitle
from tests.helper.courses_helper import course_patch_json

course_patch = CourseUpdate(**course_patch_json)


def test_crud_course_patch(course_db):
    db_session = MagicMock()

    course.patch_course(db=db_session, course_to_update=course_patch, course_db_data=course_db)


def test_crud_course_get_exams_from_courses(course_db):
    db_session = MagicMock()

    course.get_exams_from_courses(db=db_session, user_id="user_id", active_students=True, graded=True)


def test_crud_course_get_courses_with_filters(course_db):
    db_session = MagicMock()

    course.get_courses_with_filters(db=db_session, plan_filter=SubscriptionTitle.free,
                                    category_filter=CourseType.programming)

from unittest.mock import MagicMock

from app.crud import course
from app.schemas.course.course import CourseUpdate
from tests.helper.courses_helper import course_patch_json, course_db

course_patch = CourseUpdate(**course_patch_json)


def test_crud_course_patch():
    db_session = MagicMock()

    course.patch_course(db=db_session, course_to_update=course_patch, course_db_data=course_db)

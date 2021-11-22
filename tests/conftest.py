import pytest
from starlette.testclient import TestClient

from app.main import app
from app.models.user import UserAccount
from app.models.course import Course
from app.models.enroll_course import EnrollCourse
from tests.helper.courses_helper import course_db_json
from tests.helper.exams_helper import course_exam_db_json
from tests.helper.enroll_course_helper import enroll_course_db_json
from tests.helper.users_helper import complete_user_info_db_json, \
    user_info_extra_data_db_json


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def user_complete_db():
    return UserAccount(**complete_user_info_db_json)


@pytest.fixture(scope="module")
def user_extra_data_db():
    return UserAccount(**user_info_extra_data_db_json)


@pytest.fixture(scope="module")
def course_db():
    return Course(**course_db_json)


@pytest.fixture(scope="module")
def course_with_exam_db():
    return Course(**course_exam_db_json)


@pytest.fixture(scope="module")
def student_db():
    return EnrollCourse(**enroll_course_db_json)

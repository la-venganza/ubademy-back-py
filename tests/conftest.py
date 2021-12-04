from datetime import date

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.models.user import UserAccount
from app.models.course import Course
from app.models.enroll_course import EnrollCourse
from app.models.subscription import Subscription
from app.models.user_subscription import UserSubscription
from tests.helper.courses_helper import course_db_json, course_exam_with_enrollment_with_exams_db_json
from tests.helper.exams_helper import course_exam_db_json
from tests.helper.enroll_course_helper import enroll_course_db_json
from tests.helper.user_subscription_helpler import user_subscription_info_db_json,\
    free_subscription_db_json, user_subscription_inactive_db_json
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


@pytest.fixture(scope="module")
def free_subscription_db():
    return Subscription(**free_subscription_db_json)


@pytest.fixture(scope="module")
def user_subscription_db():
    user_subscription = UserSubscription(**user_subscription_info_db_json)
    user_subscription.end_date = date.fromisoformat(user_subscription.end_date)
    return user_subscription


@pytest.fixture(scope="module")
def user_inactive_subscription_db():
    return UserSubscription(**user_subscription_inactive_db_json)


@pytest.fixture(scope="module")
def course_with_enrollments_with_exam_db():
    return Course(**course_exam_with_enrollment_with_exams_db_json)

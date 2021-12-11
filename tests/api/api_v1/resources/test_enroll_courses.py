import json

from app.api.api_v1.resources import enroll_courses
from app.crud import course, user, enroll_course
from tests.helper.enroll_course_helper import enroll_course_response_json, course_registration_json
from tests.helper.user_subscription_helpler import gold_subscription_db, premium_subscription_db


# ------------------ Course registration ------------------------ #
def test_course_registration_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.post("/api/v1/courses/1/registration", data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_registration_user_id_not_found(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_registration_user_already_register(test_app, user_extra_data_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 400
    assert response.json() == {'detail': 'User 1 is already register in course 1'}


def test_course_registration_user_subscription_not_good_enough(test_app, user_complete_db, course_gold_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_gold_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'The course with id 1 requires a Gold subscription'
                                         ' and user 1 has a Free subscription'}


def test_course_registration_ok(test_app, user_complete_db, course_db, student_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(enroll_course, 'create', return_value=student_db)
    response = test_app.post("/api/v1/courses/2/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 200
    assert response.json() == enroll_course_response_json


def test_course_registration_user_inactive_registration_ok(
        test_app, user_extra_data_inactive_student_db, course_db, student_db, mocker
):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_inactive_student_db)
    mocker.patch.object(enroll_course, 'update', return_value=student_db)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 200
    assert response.json() == enroll_course_response_json


# ------------------ Course disenroll ------------------------ #
def test_course_disenroll_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.patch("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_disenrol_user_id_not_found(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id',
                        return_value=None)
    response = test_app.patch("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_disenrol_user_not_register(test_app, user_complete_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    response = test_app.patch("/api/v1/courses/1/registration", data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'User 1 is not register in course 1'}


def test_course_disenrol_ok(test_app, user_extra_data_db, course_db, student_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(enroll_course, 'update', return_value=student_db)
    response = test_app.patch("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 200
    assert response.json() == enroll_course_response_json


# -------------------------- validate user subscription against course subscription ------------ #
def test_validate_user_subscription_against_course_subscription_free_ok(free_subscription_db):
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=free_subscription_db,
        course_subscription_required=free_subscription_db)
    assert result


def test_validate_user_subscription_against_course_subscription_free_failed_gold(free_subscription_db):
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=free_subscription_db,
        course_subscription_required=gold_subscription_db)
    assert not result


def test_validate_user_subscription_against_course_subscription_free_failed_premium(free_subscription_db):
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=free_subscription_db,
        course_subscription_required=premium_subscription_db)
    assert not result


def test_validate_user_subscription_against_course_subscription_gold_ok_free(free_subscription_db):
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=gold_subscription_db,
        course_subscription_required=free_subscription_db)
    assert result


def test_validate_user_subscription_against_course_subscription_gold_ok_gold():
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=gold_subscription_db,
        course_subscription_required=gold_subscription_db)
    assert result


def test_validate_user_subscription_against_course_subscription_gold_failed_premium():
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=gold_subscription_db,
        course_subscription_required=premium_subscription_db)
    assert not result


def test_validate_user_subscription_against_course_subscription_premium_ok_free(free_subscription_db):
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=premium_subscription_db,
        course_subscription_required=free_subscription_db)
    assert result


def test_validate_user_subscription_against_course_subscription_premium_ok_gold():
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=premium_subscription_db,
        course_subscription_required=gold_subscription_db)
    assert result


def test_validate_user_subscription_against_course_subscription_premium_ok_premium():
    result = enroll_courses.validate_user_subscription_against_course_subscription(
        user_subscription=premium_subscription_db,
        course_subscription_required=premium_subscription_db)
    assert result

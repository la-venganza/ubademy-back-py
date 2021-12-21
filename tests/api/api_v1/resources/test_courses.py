import json

from app.crud import course, user, collaborator, subscription
from app.models.user import UserAccount
from app.schemas.course.course import CourseType
from tests.helper.collaborator_helper import collaborator_response_json, collaborator_db_json, \
    course_collaboration_rq_json, other_course_collaboration_rq_json
from tests.helper.courses_helper import course_response_json, other_course_db, course_to_create_json, \
    course_patch_json, course_basics_response_json, course_global_basics_response_json


# ------------------ Courses get with filters ------------------------ #
def test_courses_invalid_keyword(test_app):
    response = test_app.get("/api/v1/courses?keyword=aa")
    assert response.status_code == 422


def test_courses_ok_no_users(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[])
    response = test_app.get("/api/v1/courses")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_courses_ok_filters_case_ingore_ok(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[])
    response = test_app.get("/api/v1/courses?category=programming")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_courses_ok_filters_case_ingore2_ok(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[])
    response = test_app.get("/api/v1/courses?category=PrograMmIng")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_courses_ok_with_results(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses")
    assert response.status_code == 200
    assert response.json() == {'results': [course_basics_response_json, course_basics_response_json]}


def test_courses_ok_filter(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses?keyword=java")
    assert response.status_code == 200
    assert response.json() == {'results': [course_basics_response_json, course_basics_response_json]}


def test_courses_ok_filter_with_max_results(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses?keyword=java&max_results=1")
    assert response.status_code == 200
    assert response.json() == {'results': [course_basics_response_json]}


def test_courses_ok_filter_with_max_results_ignore(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses?plan=Free&max_results=1")
    assert response.status_code == 200
    assert response.json() == {'results': [course_basics_response_json, course_basics_response_json]}


def test_courses_ok_pagination_invalid_page_value(test_app):
    response = test_app.get("/api/v1/courses?page_size=1&page=0")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page value must be at least 1'}


def test_courses_ok_pagination_invalid_page_size(test_app):
    response = test_app.get("/api/v1/courses?page_size=0&page=1")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page size must be at least 1'}


def test_courses_ok_pagination(test_app, course_db, mocker):
    mocker.patch.object(course, 'get_courses_with_filters', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses?page_size=1&page=1")
    assert response.status_code == 200
    assert response.json() == {'results': [course_basics_response_json, course_basics_response_json]}


# ------------------ Course post ------------------------ #
def test_courses_create_ok(test_app, course_db, free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=UserAccount())
    mocker.patch.object(subscription, "get_by_subscription_plan", return_value=free_subscription_db)
    mocker.patch.object(course, 'create', return_value=course_db)
    response = test_app.post("/api/v1/courses", data=json.dumps(course_to_create_json))
    assert response.status_code == 201
    assert response.json() == course_response_json


def test_courses_fail_create_user_not_exists(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.post("/api/v1/courses", data=json.dumps(course_to_create_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


# ------------------ Course get by id ------------------------ #
def test_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.get("/api/v1/courses/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The course with id 1 was not found'}


def test_course_ok(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    response = test_app.get("/api/v1/courses/1")
    assert response.status_code == 200
    assert response.json() == course_response_json


def test_course_ok_basic_not_student(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    response = test_app.get("/api/v1/courses/1?user_id=fake")
    assert response.status_code == 200
    assert response.json() == course_global_basics_response_json


# ------------------ Course collaboration ------------------------ #
def test_course_collaboration_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_rq_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_collaboration_user_id_not_found(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id',
                        return_value=None)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_rq_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 2 was not found'}


def test_course_collaboration_user_already_register(test_app, user_extra_data_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_rq_json))
    assert response.status_code == 400
    assert response.json() == {'detail': 'User 2 is already collaborating in course 1'}


def test_course_collaboration_user_not_creator(test_app, user_complete_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(collaborator, "create", return_value=collaborator_db_json)
    response = test_app.post("/api/v1/courses/2/collaboration",
                             data=json.dumps(other_course_collaboration_rq_json))
    assert response.status_code == 403
    assert response.json() == {'detail':  'Course with id 2 can only be edited by it\'s creator'}


def test_course_collaboration_ok(test_app, user_complete_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(collaborator, "create", return_value=collaborator_db_json)
    response = test_app.post("/api/v1/courses/2/collaboration",
                             data=json.dumps(course_collaboration_rq_json))
    assert response.status_code == 200
    assert response.json() == collaborator_response_json


# ------------------ Course patch ------------------------ #
def test_course_patch_course_not_found(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_patch_user_id_not_found(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_patch_uer_not_creator_of_course(test_app, user_complete_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=other_course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'User with id 1 is not the creator of course with id 1'}


def test_course_patch_ok(test_app, user_complete_db, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(course, 'patch_course', return_value=course_db)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 200
    assert response.json() == course_response_json


def test_courses_types(test_app):
    response = test_app.get("/api/v1/courses/types")
    assert response.status_code == 200
    assert response.json() == {'course_types': CourseType.list()}


def test_course_types_name_ignore_case():
    assert CourseType["programming"] == CourseType.programming
    assert CourseType["Programming"] == CourseType.programming
    assert CourseType["progrAMming"] == CourseType.programming

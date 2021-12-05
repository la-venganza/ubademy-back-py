from app.crud import course
from tests.helper.courses_helper import course_exam_with_enrollment_db, course_with_enrollment_with_answered_exam_db, \
    search_exams_response_json


# ------------------ Exams publish by students search ------------------------ #
def test_search_exams_no_userId(test_app):
    response = test_app.get("/api/v1/courses/lessons/exams")
    assert response.status_code == 422


def test_search_exams_active_students_invalid(test_app):
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds&active_students=rr")
    assert response.status_code == 422


def test_search_exams_graded_status_invalid(test_app):
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds&graded_status=rr")
    assert response.status_code == 422


def test_search_exams_ok_no_exams(test_app, mocker):
    mocker.patch.object(course, 'get_exams_from_courses', return_value=[])
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_search_exams_ok_no_exams(test_app, mocker):
    mocker.patch.object(course, 'get_exams_from_courses', return_value=[course_exam_with_enrollment_db])
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_search_exams_ok(test_app, mocker):
    mocker.patch.object(course, 'get_exams_from_courses', return_value=[course_with_enrollment_with_answered_exam_db])
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=1")
    assert response.status_code == 200
    assert response.json() == {'results': [search_exams_response_json]}


# ------------------ Exams publish by students search - pagination ------------------------ #
def test_search_exams_ok_pagination_invalid_page_value(test_app):
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds&page_size=1&page=0")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page value must be at least 1'}


def test_search_exams_ok_pagination_invalid_page_size(test_app):
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=afds&page_size=0&page=1")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page size must be at least 1'}


def test_search_exams_ok_pagination(test_app, mocker):
    mocker.patch.object(
        course, 'get_exams_from_courses',
        return_value=[course_with_enrollment_with_answered_exam_db, course_with_enrollment_with_answered_exam_db])
    response = test_app.get("/api/v1/courses/lessons/exams?user_id=1&page_size=1&page=1")
    assert response.status_code == 200
    assert response.json() == {'results': [search_exams_response_json, search_exams_response_json]}

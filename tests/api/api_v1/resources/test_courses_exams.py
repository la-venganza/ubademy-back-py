from app.crud import course
from tests.helper.courses_helper import course_exam_with_enrollment_db, course_with_enrollment_with_answered_exam_db, \
    search_exams_response_json


# ------------------ Exams publish by students search ------------------------ #
def test_search_exams_no_user_id(test_app):
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


# ------------------ Exams from course search ------------------------ #
def test_search_course_exams_no_user_id(test_app):
    response = test_app.get("/api/v1/courses/1/lessons/exams")
    assert response.status_code == 422


def test_search_course_exams_not_staff(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=afds")
    assert response.status_code == 403
    assert response.json() ==\
           {'detail': 'Exams of course with id 1 can only be listed for it\'s creator or a collaborator'}


def test_search_course_exams_ok_no_exams(test_app, course_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=1")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_search_course_exams_ok(test_app, exam_basics, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_with_enrollment_db)
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=1")
    assert response.status_code == 200
    assert response.json() == {'results': [exam_basics]}


# ------------------ Exams from course search - pagination ------------------------ #
def test_search_course_exams_pagination_invalid_page_value(test_app):
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=afds&page_size=1&page=0")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page value must be at least 1'}


def test_search_course_exams_pagination_invalid_page_size(test_app):
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=afds&page_size=0&page=1")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Page size must be at least 1'}


def test_search_course_exams_pagination_ok(test_app, exam_basics, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_with_enrollment_db)
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=1&page_size=1&page=1")
    assert response.status_code == 200
    assert response.json() == {'results': [exam_basics]}


def test_search_course_exams_pagination_ok_page_with_no_values(test_app, exam_basics, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_with_enrollment_db)
    response = test_app.get("/api/v1/courses/1/lessons/exams?user_id=1&page_size=1&page=2")
    assert response.status_code == 200
    assert response.json() == {'results': []}

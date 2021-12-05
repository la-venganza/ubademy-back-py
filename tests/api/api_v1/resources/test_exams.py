import json

from tests.helper.courses_helper import course_exam_with_enrollment_db
from tests.helper.exams_helper import exam_db_created, exam_to_create_json, exam_response_json, \
    exam_to_create_invalid_user_json, exam_patch_json, exam_patch_invalid_user_json, course_exam_db, exam_publish_json,\
    enroll_course_exam_response_json, exam_publish_grade_invalid_json, exam_publish_grade_json, \
    exam_publish_grade_other_json
from app.crud import course, exam, lesson, enroll_course_exam


# ------------------ Exam post ------------------------ #
def test_exams_create_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    mocker.patch.object(exam, 'create', return_value=exam_db_created)
    mocker.patch.object(lesson, 'update_lesson')
    response = test_app.post("/api/v1/courses/1/lessons/1/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 201
    assert response.json() == exam_response_json


def test_exams_create_fail_no_course(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=None)
    response = test_app.post("/api/v1/courses/1/lessons/1/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 404
    assert response.json() =={'detail': 'Course with id 1 was not found'}


def test_exams_create_fail_no_lesson(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.post("/api/v1/courses/1/lessons/3/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 404
    assert response.json() =={'detail': 'The lesson with id 3 was not found'}


def test_exams_create_fail_lesson_already_has_an_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)

    response = test_app.post("/api/v1/courses/1/lessons/2/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 400
    assert response.json() =={'detail': 'An exam already exists for lesson 2 and course 1'}


def test_exams_create_fail_user_is_not_creator(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    mocker.patch.object(exam, 'create', return_value=exam_db_created)
    mocker.patch.object(lesson, 'update_lesson')
    response = test_app.post("/api/v1/courses/1/lessons/1/exams/", data=json.dumps(exam_to_create_invalid_user_json))
    assert response.status_code == 403
    assert response.json() =={'detail': 'Course with id 1 can only be edited by it\'s creator'}


# ------------------ Exam get by id ------------------------ #
def test_exam_not_found_no_course(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=None)
    response = test_app.get("/api/v1/courses/1/lessons/1/exams/3")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_exams_get_fail_no_lesson(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.get("/api/v1/courses/1/lessons/3/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The lesson with id 3 was not found'}


def test_exams_get_fail_no_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.get("/api/v1/courses/1/lessons/1/exams/11", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The exam with id 11 was not found'}


def test_exam_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.get("/api/v1/courses/1/lessons/2/exams/1")
    assert response.status_code == 200
    assert response.json() == exam_response_json


# ------------------ Exam patch ------------------------ #
def test_exams_update_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    mocker.patch.object(exam, 'patch_exam', return_value=exam_db_created)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 200
    assert response.json() == exam_response_json


def test_exams_update_fail_no_course(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=None)
    response = test_app.patch("/api/v1/courses/1/lessons/1/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_exams_update_fail_no_lesson(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.patch("/api/v1/courses/1/lessons/3/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The lesson with id 3 was not found'}


def test_exams_update_fail_no_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.patch("/api/v1/courses/1/lessons/1/exams/11", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The exam with id 11 was not found'}


def test_exams_update_fail_user_is_not_creator(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    mocker.patch.object(lesson, 'update_lesson')
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1", data=json.dumps(exam_patch_invalid_user_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'Course with id 1 can only be edited by it\'s creator'}


# ------------------ Publish exam for student by id ------------------------ #
def test_publish_exam_not_found_no_course(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=None)
    response = test_app.post("/api/v1/courses/1/lessons/1/exams/3/solution", data=json.dumps(exam_publish_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_publish_exam_post_fail_no_lesson(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.post("/api/v1/courses/1/lessons/3/exams/1/solution", data=json.dumps(exam_publish_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The lesson with id 3 was not found'}


def test_publish_exam_post_fail_no_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.post("/api/v1/courses/1/lessons/1/exams/11/solution", data=json.dumps(exam_publish_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The exam with id 11 was not found'}


def test_publish_exam_post_fail_not_enrolled(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_db)
    response = test_app.post("/api/v1/courses/1/lessons/2/exams/1/solution", data=json.dumps(exam_publish_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'The user with id 1 is not enrolled to course 1'}


def test_publish_exam_post_ok(test_app, enroll_course_exam_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_exam_with_enrollment_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_with_enrollment_db)
    mocker.patch.object(enroll_course_exam, 'create', return_value=enroll_course_exam_db)
    response = test_app.post("/api/v1/courses/1/lessons/2/exams/1/solution", data=json.dumps(exam_publish_json))
    assert response.status_code == 200
    assert response.json() == enroll_course_exam_response_json


# ------------------ Publish student grade for exam published ------------------------ #
def test_publish_exam_grade_patch_invalid_grade(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_exam_with_enrollment_db)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1/solution",
                              data=json.dumps(exam_publish_grade_invalid_json))
    assert response.status_code == 422


def test_publish_exam_grade_patch_invalid_not_staff(test_app, course_with_enrollments_with_exam_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_with_enrollments_with_exam_db)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1/solution",
                              data=json.dumps(exam_publish_grade_other_json))
    assert response.status_code == 403
    assert response.json() == \
           {'detail': 'Exams of course with id 1 can only be graded by it\'s creator or a collaborator'}


def test_publish_exam_grade_patch_invalid_no_enroll_course_exam(test_app, course_with_enrollments_with_exam_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(enroll_course_exam, 'get', return_value=None)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1/solution",
                              data=json.dumps(exam_publish_grade_json))
    assert response.status_code == 400
    assert response.json() == \
           {'detail': 'Some information is invalid. There is no exam to grade for course_id 1, lesson_id 2, '
                      'exam_id 1, exam_to_grade_id 7 and enroll_course_exam_id 1'}


def test_publish_exam_grade_patch_invalid_mismatch_information(
        test_app, enroll_course_exam_db, course_with_enrollments_with_exam_db, mocker):
    mocker.patch.object(course, 'get', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(enroll_course_exam, 'get', return_value=enroll_course_exam_db)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1/solution",
                              data=json.dumps(exam_publish_grade_json))
    assert response.status_code == 400
    assert response.json() == \
           {'detail': 'Some information is invalid. There is no exam to grade for course_id 1, lesson_id 2, '
                      'exam_id 1, exam_to_grade_id 7 and enroll_course_exam_id 1'}


def test_publish_exam_grade_patch_ok(test_app, enroll_course_exam_db, course_with_enrollments_with_exam_db, mocker):
    enroll_course_exam_db.id = 7
    enroll_course_exam_db.exam_id = 1
    enroll_course_exam_db.lesson_id = 2
    mocker.patch.object(course, 'get', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_with_enrollments_with_exam_db)
    mocker.patch.object(enroll_course_exam, 'get', return_value=enroll_course_exam_db)
    enroll_course_exam_db.id = 1
    mocker.patch.object(enroll_course_exam, 'update', return_value=enroll_course_exam_db)
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1/solution",
                              data=json.dumps(exam_publish_grade_json))
    assert response.status_code == 200
    assert response.json() == enroll_course_exam_response_json

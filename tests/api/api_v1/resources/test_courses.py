import json

from app.crud import course
from app.models.course import Course
from app.crud import user
from app.models.user import UserAccount

course_db_json = json.loads(
    '{ \
      "title": "Curso Java", \
      "description": "Venis a aprender", \
      "type": "DEV", \
      "hashtags": "java, whatsapp, back, develop", \
      "location": "internet", \
      "lessons": [ \
        { \
          "id" : 1,  \
          "course_id" : 1,  \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": "1235", \
          "multimedia_type": "pdf" \
        } \
      ], \
      "id": 1, \
      "creator_id": "1" \
    }'
)


course_response_json = json.loads(
    '{ \
      "title": "Curso Java", \
      "description": "Venis a aprender", \
      "type": "DEV", \
      "hashtags": "java, whatsapp, back, develop", \
      "location": "internet", \
      "lessons": [ \
        { \
          "id" : 1,  \
          "course_id" : 1,  \
          "exam": null, \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": "1235", \
          "multimedia_type": "pdf" \
        } \
      ], \
      "id": 1, \
      "creator_id": "1" \
    }'
)

other_course_db_json = json.loads(
    '{ \
      "title": "Curso fake", \
      "description": "descripcion", \
      "type": "DEV", \
      "hashtags": "nothing, interesting, water", \
      "location": "internet", \
      "lessons": [ \
        { \
          "id" : 1,  \
          "course_id" : 2,  \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": "1235", \
          "multimedia_type": "pdf" \
        } \
      ], \
      "id": 2, \
      "creator_id": "10" \
    }'
)

course_to_create_json = json.loads(
    '{ \
      "title": "Curso Java", \
      "description": "Venis a aprender", \
      "type": "DEV", \
      "hashtags": "java, whatsapp, back, develop", \
      "location": "internet", \
      "lessons": [ \
        { \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": "1235", \
          "multimedia_type": "pdf" \
        } \
      ], \
      "user_id": "1" \
    }'
)

course_registration_json = json.loads(
    '{"user_id" : "1"}'
)

course_collaboration_json = course_registration_json

complete_user_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "blocked": false, \
      "created_courses": [], \
      "attending_courses": [  \
        { \
          "title": "Curso Java", \
          "description": "Venis a aprender", \
          "type": "DEV", \
          "hashtags": "java, whatsapp, back, develop", \
          "location": "internet", \
          "lessons": [ \
            { \
              "require": true, \
              "active": true, \
              "sequence_number": 1, \
              "multimedia_id": "1235", \
              "multimedia_type": "pdf" \
            } \
        ], \
        "id": 1, \
        "creator_id": "1" \
        } \
      ], \
      "collaborating_courses": [  \
        { \
          "title": "Curso Java", \
          "description": "Venis a aprender", \
          "type": "DEV", \
          "hashtags": "java, whatsapp, back, develop", \
          "location": "internet", \
          "lessons": [ \
            { \
              "require": true, \
              "active": true, \
              "sequence_number": 1, \
              "multimedia_id": "1235", \
              "multimedia_type": "pdf" \
            } \
        ], \
        "id": 1, \
        "creator_id": "1" \
        } \
      ] \
    }'
)

course_patch_json = json.loads(
    '{  \
        "user_id" : "1",  \
        "course" : { \
          "title": "Curso Java", \
          "description": "Venis a aprender", \
          "type": "DEV", \
          "hashtags": "java, whatsapp, back, develop", \
          "location": "internet", \
          "lessons": [ \
            { \
              "id" : 1, \
              "require": true, \
              "active": true, \
              "sequence_number": 1, \
              "multimedia_id": "1235", \
              "multimedia_type": "pdf" \
            } \
          ] \
        } \
    }'
)

course_db = Course(**course_db_json)
other_course_db = Course(**other_course_db_json)
user_db = UserAccount(**complete_user_info_db_json)
course_updated_db = Course(**course_patch_json.get("course"))


# ------------------ Courses get with filters ------------------------ #
def test_courses_invalid_keyword(test_app):
    response = test_app.get("/api/v1/courses?keyword=aa")
    assert response.status_code == 422


def test_courses_ok_no_users(test_app, mocker):
    mocker.patch.object(course, 'get_multi', return_value=[])
    response = test_app.get("/api/v1/courses")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_courses_ok_with_results(test_app, mocker):
    mocker.patch.object(course, 'get_multi', return_value=[course_db, course_db])
    response = test_app.get("/api/v1/courses")
    assert response.status_code == 200
    assert response.json() == {'results': [course_response_json, course_response_json]}


def test_courses_ok_filter(test_app, mocker):
    mocker.patch.object(course, 'get_multi', return_value=[course_db, other_course_db])
    response = test_app.get("/api/v1/courses?keyword=java")
    assert response.status_code == 200
    assert response.json() == {'results': [course_response_json]}


# ------------------ Course post ------------------------ #
def test_courses_create_ok(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=UserAccount())
    mocker.patch.object(course, 'create', return_value=course_db)
    response = test_app.post("/api/v1/courses/", data=json.dumps(course_to_create_json))
    assert response.status_code == 201
    assert response.json() == course_response_json


def test_courses_fail_create_user_not_exists(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.post("/api/v1/courses/", data=json.dumps(course_to_create_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


# ------------------ Course get by id ------------------------ #
def test_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=None)
    response = test_app.get("/api/v1/courses/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The course with id 1 was not found'}


def test_course_ok(test_app, mocker):
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.get("/api/v1/courses/1")
    assert response.status_code == 200
    assert response.json() == course_response_json


# ------------------ Course registration ------------------------ #
def test_course_registration_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_registration_user_id_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id',
                        return_value=None)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_registration_user_already_register(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    response = test_app.post("/api/v1/courses/1/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 400
    assert response.json() == {'detail': 'User 1 is already register in course 1'}


def test_course_registration_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    mocker.patch.object(user, 'update_user')
    response = test_app.post("/api/v1/courses/2/registration",
                             data=json.dumps(course_registration_json))
    assert response.status_code == 200
    assert response.json() == course_response_json


# ------------------ Course collaboration ------------------------ #
def test_course_collaboration_course_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_collaboration_user_id_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id',
                        return_value=None)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_collaboration_user_already_register(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    response = test_app.post("/api/v1/courses/1/collaboration",
                             data=json.dumps(course_collaboration_json))
    assert response.status_code == 400
    assert response.json() == {'detail': 'User 1 is already collaborating in course 1'}


def test_course_collaboration_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    mocker.patch.object(user, 'update_user')
    response = test_app.post("/api/v1/courses/2/collaboration",
                             data=json.dumps(course_collaboration_json))
    assert response.status_code == 200
    assert response.json() == course_response_json


# ------------------ Course patch ------------------------ #
def test_course_patch_course_not_found(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    mocker.patch.object(course, 'get', return_value=None)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course with id 1 was not found'}


def test_course_patch_user_id_not_found(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_course_patch_uer_not_creator_of_course(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=other_course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'User with id 1 is not the creator of course with id 1'}


def test_course_patch_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(user, 'get_by_user_id', return_value=user_db)
    mocker.patch.object(course, 'patch_course', return_value=course_db)
    response = test_app.patch("/api/v1/courses/1", data=json.dumps(course_patch_json))
    assert response.status_code == 200
    assert response.json() == course_response_json

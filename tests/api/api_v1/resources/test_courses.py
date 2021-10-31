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
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": 1235 \
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
          "exam": null, \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": 1235 \
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
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": 1235 \
        } \
      ], \
      "id": 2, \
      "creator_id": "1" \
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
          "multimedia_id": 1235 \
        } \
      ], \
      "user_id": "1" \
    }'
)

course_db = Course(**course_db_json)
other_course_db = Course(**other_course_db_json)


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


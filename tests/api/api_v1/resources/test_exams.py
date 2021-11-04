import json

from app.crud import course, exam, lesson
from app.models.course import Course, Exam
from app.models.user import UserAccount

course_db_json = json.loads(
    '{ \
       "title":"Curso Java", \
       "description":"Venis a aprender", \
       "type":"DEV", \
       "hashtags":"java, backend, back, develop", \
       "location":"internet", \
       "lessons":[ \
          { \
             "id": 1, \
             "require": true, \
             "active":true, \
             "sequence_number":1, \
             "multimedia_id":1235, \
             "exam":"None" \
          }, \
          { \
             "id": 2, \
             "require":true, \
             "active":true, \
             "sequence_number":2, \
             "multimedia_id":1236, \
             "exam":{ \
                "id": 1, \
                "title": "title", \
                "description": "description", \
                "minimum_qualification": 6, \
                "creation_date": "2021-10-31T04:11:49.435796+00:00", \
                "questions": [ \
                  { \
                    "id": 1, \
                    "exam_id": 1, \
                    "sequence_number": 1, \
                    "type": "Choice", \
                    "score": 8, \
                    "multiple_choice_question": { \
                    "id": 1, \
                      "question_id": 1, \
                      "text": "hola", \
                      "amount_of_options": 1, \
                      "choices": [ \
                        { \
                          "id": 1, \
                          "multiple_choice_question_id": 1, \
                          "text": "Que paso", \
                          "is_correct": true \
                        } \
                      ] \
                    } \
                  } \
                ] \
            } \
          } \
       ], \
        "id": 1, \
        "creator_id": "1" \
    }'
)

exam_db_json = json.loads(
    '{ \
      "title": "Examen Java", \
      "description": "Dependency injection exam", \
      "minimum_qualification": 7, \
      "questions": [ \
      { \
       "sequence_number": 2, \
       "type": "Choice", \
       "score": 9, \
        "multiple_choice_question": { \
        "text": "Algun framework para manejar dependency injections?", \
        "amount_of_options": 3, \
        "choices": [ \
          { \
            "text": "Spring", \
            "is_correct": true, \
            "id": 1, \
            "multiple_choice_question_id": 1 \
            }, \
          { \
            "text": "Hibernate", \
            "is_correct": false, \
            "id": 2, \
            "multiple_choice_question_id": 1 \
          } \
        ], \
        "id": 1, \
        "question_id": 2 \
        }, \
         "develop_question": null, \
         "id": 2, \
         "exam_id": 1 \
         }, \
         { \
          "sequence_number": 1, \
          "type": "Develop", \
          "score": 1, \
          "multiple_choice_question": null, \
          "develop_question": { \
          "text": "Que significa injection dependency?", \
          "id": 1, \
          "question_id": 1 \
          }, \
          "id": 1, \
          "exam_id": 1 \
          } \
        ], \
        "id": 1, \
        "creation_date": "2021-10-31T04:11:49.435796+00:00" \
    }'
)


exam_response_json = json.loads(
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

exam_to_create_json = json.loads(
    '{ \
      "user_id": "1", \
      "exam": { \
        "title": "title", \
        "description": "description", \
        "minimum_qualification": 6, \
        "questions": [ \
          { \
            "sequence_number": 1, \
            "type": "Choice", \
            "score": 8, \
            "multiple_choice_question": { \
              "text": "hola", \
              "amount_of_options": 1, \
              "choices": [ \
                { \
                  "text": "Que paso", \
                  "is_correct": true \
                } \
              ] \
            } \
          } \
        ] \
      } \
    }'
)

exam_to_create_invalid_user_json = json.loads(
    '{ \
      "user_id": "10", \
      "exam": { \
        "title": "title", \
        "description": "description", \
        "minimum_qualification": 6, \
        "questions": [ \
          { \
            "sequence_number": 1, \
            "type": "Choice", \
            "score": 8, \
            "multiple_choice_question": { \
              "text": "hola", \
              "amount_of_options": 1, \
              "choices": [ \
                { \
                  "text": "Que paso", \
                  "is_correct": true \
                } \
              ] \
            } \
          } \
        ] \
      } \
    }'
)

exam_to_create_db_json = json.loads(
    '{ \
        "id": 1, \
        "title": "title", \
        "description": "description", \
        "minimum_qualification": 6, \
        "creation_date": "2021-10-31T04:11:49.435796+00:00", \
        "questions": [ \
          { \
            "id": 1, \
            "exam_id": 1, \
            "sequence_number": 1, \
            "type": "Choice", \
            "score": 8, \
            "multiple_choice_question": { \
            "id": 1, \
              "question_id": 1, \
              "text": "hola", \
              "amount_of_options": 1, \
              "choices": [ \
                { \
                  "id": 1, \
                  "multiple_choice_question_id": 1, \
                  "text": "Que paso", \
                  "is_correct": true \
                } \
              ] \
            } \
          } \
        ] \
    }'
)

exam_response_json = json.loads(
    '{ \
    "id": 1, \
    "title": "title", \
    "description": "description", \
    "minimum_qualification": 6, \
    "creation_date": "2021-10-31T04:11:49.435796+00:00", \
    "questions": [ \
      { \
        "id": 1, \
        "exam_id": 1, \
        "sequence_number": 1, \
        "type": "Choice", \
        "score": 8, \
        "develop_question": null, \
        "multiple_choice_question": { \
          "id": 1, \
          "question_id": 1, \
          "text": "hola", \
          "amount_of_options": 1, \
          "choices": [ \
            { \
              "id": 1, \
              "multiple_choice_question_id": 1, \
              "text": "Que paso", \
              "is_correct": true \
            } \
          ] \
        } \
      } \
    ] \
    }'
)


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

exam_patch_json = json.loads(
    '{  \
        "user_id" : "1",  \
        "exam" : { \
            "title": "Other title", \
            "description": "description", \
            "minimum_qualification": 6, \
            "questions": [ \
              { \
                "id": 1, \
                "sequence_number": 1, \
                "type": "Choice", \
                "score": 9, \
                "multiple_choice_question": { \
                  "id": 1, \
                  "text": "hola", \
                  "amount_of_options": 1, \
                  "choices": [ \
                    { \
                      "id": 1, \
                      "text": "Que paso", \
                      "is_correct": true \
                    } \
                  ] \
                } \
              } \
            ] \
          } \
    }'
)

exam_patch_invalid_user_json = json.loads(
    '{  \
        "user_id" : "10",  \
        "exam" : { \
            "title": "Other title", \
            "description": "description", \
            "minimum_qualification": 6, \
            "questions": [ \
              { \
                "id": 1, \
                "sequence_number": 1, \
                "type": "Choice", \
                "score": 9, \
                "multiple_choice_question": { \
                  "id": 1, \
                  "text": "hola", \
                  "amount_of_options": 1, \
                  "choices": [ \
                    { \
                      "id": 1, \
                      "text": "Que paso", \
                      "is_correct": true \
                    } \
                  ] \
                } \
              } \
            ] \
          } \
    }'
)

course_db = Course(**course_db_json)
exam_db = Exam(**exam_db_json)
exam_db_created = Exam(**exam_to_create_db_json)
user_db = UserAccount(**complete_user_info_db_json)
exam_updated_db = Exam(**exam_patch_json.get("exam"))


# ------------------ Exam post ------------------------ #
def test_exams_create_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
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
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.post("/api/v1/courses/1/lessons/3/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 404
    assert response.json() =={'detail': 'The lesson with id 3 was not found'}


def test_exams_create_fail_lesson_already_has_an_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)

    response = test_app.post("/api/v1/courses/1/lessons/2/exams/", data=json.dumps(exam_to_create_json))
    assert response.status_code == 400
    assert response.json() =={'detail': 'An exam already exists for lesson 2 and course 1'}


def test_exams_create_fail_user_is_not_creator(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
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
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.get("/api/v1/courses/1/lessons/3/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The lesson with id 3 was not found'}


def test_exams_get_fail_no_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.get("/api/v1/courses/1/lessons/1/exams/11", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The exam with id 11 was not found'}


def test_exam_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.get("/api/v1/courses/1/lessons/2/exams/1")
    assert response.status_code == 200
    assert response.json() == exam_response_json


# ------------------ Exam patch ------------------------ #
def test_exams_update_ok(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
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
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.patch("/api/v1/courses/1/lessons/3/exams/1", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The lesson with id 3 was not found'}


def test_exams_update_fail_no_exam(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    response = test_app.patch("/api/v1/courses/1/lessons/1/exams/11", data=json.dumps(exam_patch_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The exam with id 11 was not found'}


def test_exams_update_fail_user_is_not_creator(test_app, mocker):
    mocker.patch.object(course, 'get', return_value=course_db)
    mocker.patch.object(course, 'get_full_by_course_id', return_value=course_db)
    mocker.patch.object(lesson, 'update_lesson')
    response = test_app.patch("/api/v1/courses/1/lessons/2/exams/1", data=json.dumps(exam_patch_invalid_user_json))
    assert response.status_code == 403
    assert response.json() == {'detail': 'Course with id 1 can only be edited by it\'s creator'}

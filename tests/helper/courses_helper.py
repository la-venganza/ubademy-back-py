import json

from app.models.course import Course

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
          "title" : "title",  \
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

lesson_db_of_course_json = json.loads(
    '{ \
          "id" : 1,  \
          "title" : "title",  \
          "course_id" : 1,  \
          "require": true, \
          "active": true, \
          "sequence_number": 1, \
          "multimedia_id": "1235", \
          "multimedia_type": "pdf" \
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
          "title" : "title",  \
          "description" : null, \
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
          "title" : "title",  \
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
          "title" : "title",  \
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
              "title" : "title",  \
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

course_exam_with_enrollment_db_json = json.loads(
    '{ \
       "title":"Curso Java", \
       "description":"Venis a aprender", \
       "type":"DEV", \
       "hashtags":"java, backend, back, develop", \
       "location":"internet", \
       "enrollments": [ \
        { \
              "id": 1, \
              "user_id": "1", \
              "course_id": 1, \
              "active": true, \
              "current_lesson": null, \
              "grade": null, \
              "end_date": null, \
              "start_date": "2020-01-01" \
        } \
        ], \
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
                "active": false, \
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

course_exam_with_enrollment_with_exams_db_json = json.loads(
    '{ \
       "title":"Curso Java", \
       "description":"Venis a aprender", \
       "type":"DEV", \
       "hashtags":"java, backend, back, develop", \
       "location":"internet", \
       "enrollments": [ \
        { \
              "id": 1, \
              "user_id": "1", \
              "course_id": 1, \
              "active": true, \
              "current_lesson": null, \
              "grade": null, \
              "end_date": null, \
              "start_date": "2020-01-01", \
              "user": \
                { \
                  "id": 1, \
                  "username" : "username",  \
                  "user_id": "1", \
                  "email": "some@mail.com.ar" \
                }, \
              "exams": [ \
                {  \
                    "id" : 1,  \
                    "enroll_course_id" : 1,  \
                    "lesson_id" : 1,  \
                    "exam_id" : 2,  \
                    "exam_date" : "2021-01-01T13:59:57",  \
                    "grade" : null, \
                    "enroll_course" : \
                    { \
                      "id": 1, \
                      "user_id": "1", \
                      "course_id": 1, \
                      "active": true, \
                      "current_lesson": null, \
                      "grade": null, \
                      "end_date": null, \
                      "start_date": "2020-01-01" \
                    }, \
                    "answers" : [ \
                        { \
                            "id": 1, \
                            "enroll_course_exam_id": 1, \
                            "question_id": 1, \
                            "text": "answer", \
                            "choice_id": null \
                        }, \
                        { \
                            "id": 2, \
                            "enroll_course_exam_id": 1, \
                            "question_id": 2, \
                            "choice_id": 5, \
                            "text": null \
                        } \
                    ] \
                } \
            ] \
        } \
        ], \
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
                "active": false, \
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

search_exams_response_json = json.loads(
    '{ \
      "active_student": true, \
      "course_id": 1, \
      "course_title": "Curso Java", \
      "enroll_course_id": 1, \
      "exam_date": "2021-01-01T13:59:57", \
      "exam_grade": null, \
      "exam_id": 2, \
      "exam_taken_id": 1, \
      "lesson_id": 1, \
      "student_email": "some@mail.com.ar", \
      "student_id": "1", \
      "student_username": "username" \
    }'
)

other_course_db = Course(**other_course_db_json)
course_updated_db = Course(**course_patch_json.get("course"))
course_exam_with_enrollment_db = Course(**course_exam_with_enrollment_db_json)
course_with_enrollment_with_answered_exam_db = Course(**course_exam_with_enrollment_with_exams_db_json)

import json

from app.models.course import Course, Exam
from app.models.enroll_course_exam import EnrollCourseExam

course_exam_db_json = json.loads(
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

exam_db_json = json.loads(
    '{ \
      "title": "Examen Java", \
      "description": "Dependency injection exam", \
      "active": false, \
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
    }'
)

exam_response_json = json.loads(
    '{ \
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

exam_publish_json = json.loads(
    '{  \
        "user_id" : "1",  \
        "answers" : [ \
            { \
                "question_id": 1, \
                "input_answer": "answer" \
            }, \
                         { \
                "question_id": 2, \
                "choice_id": 5 \
            } \
        ] \
    }'
)

enroll_course_exam_db_json = json.loads(
    '{  \
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
    }'
)

enroll_course_exam_response_json = json.loads(
    '{  \
        "id" : 1,  \
        "exam_date" : "2021-01-01T13:59:57", \
        "grade" : null, \
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
    }'
)

course_exam_db = Course(**course_exam_db_json)
exam_db = Exam(**exam_db_json)
exam_db_created = Exam(**exam_to_create_db_json)
exam_updated_db = Exam(**exam_patch_json.get("exam"))
enroll_course_exam_db = EnrollCourseExam(**enroll_course_exam_db_json)

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

other_course_db = Course(**other_course_db_json)
course_updated_db = Course(**course_patch_json.get("course"))

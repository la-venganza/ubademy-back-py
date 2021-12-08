import json

enroll_course_response_json = json.loads(
    '{ \
        "current_lesson": null, \
        "end_date": null, \
        "grade": null, \
        "active": true, \
        "start_date": "2020-01-01", \
        "course": { \
          "title": "Curso Java", \
          "description": "Venis a aprender", \
          "type": "Programming", \
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
          "creator_id": "1", \
          "subscription_id_required": 1, \
           "subscription_required": { \
                "id": 1, \
                "title": "Free"\
          } \
        }, \
        "user": { \
            "username": "username", \
            "role": "Owner", \
            "birth_date": "1990-01-21", \
            "subscriptions": [ \
            { \
              "active": true, \
              "end_date": null, \
              "subscription": { \
                "id": 1, \
                "title": "Free" \
              }, \
              "start_date": "2021-11-21" \
            } \
          ], \
            "user_id": "1", \
            "email": "fake@email.com", \
            "blocked": false, \
            "is_admin": true, \
            "first_name": null, \
            "last_name": null, \
            "phone_number": null, \
            "phone_type": null \
        } \
    }'

)

enroll_course_db_json = json.loads(
    '{ \
      "id": 1, \
      "user_id": "1", \
      "course_id": 1, \
      "active": true, \
      "current_lesson": null, \
      "grade": null, \
      "end_date": null, \
      "user": { \
            "id": 1, \
            "username": "username", \
            "role": "Owner", \
            "birth_date": "1990-01-21", \
            "subscriptions": [ \
            { \
              "active": true, \
              "end_date": null, \
              "subscription": { \
                "id": 1, \
                "title": "Free" \
              }, \
              "start_date": "2021-11-21" \
            } \
          ], \
            "user_id": "1", \
            "email": "fake@email.com", \
            "blocked": false, \
            "is_admin": true \
        }, \
      "course": { \
          "title": "Curso Java", \
          "description": "Venis a aprender", \
          "type": "Programming", \
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
          "creator_id": "1", \
          "subscription_id_required": 1, \
           "subscription_required": { \
                "id": 1, \
                "title": "Free"\
          } \
        }, \
      "start_date": "2020-01-01" \
    }'
)

course_registration_json = json.loads(
    '{"user_id" : "1"}'
)

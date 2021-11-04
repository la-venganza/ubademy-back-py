import json

from app.models.user import UserAccount

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
      "attending_courses": [], \
      "collaborating_courses": [] \
    }'
)

other_user_complete_user_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "filter@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "blocked": false, \
      "created_courses": [], \
      "attending_courses": [], \
      "collaborating_courses": [] \
    }'
)

complete_user_info_expected_json = json.loads(
    '{ \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "blocked": false, \
      "created_courses": [], \
      "attending_courses": [], \
      "collaborating_courses": [] \
    }'
)

basic_user_info_json = json.loads(
    '{ \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "blocked": false \
    }'
)

user_info_extra_data_db_json = json.loads(
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

user_complete_db = UserAccount(**complete_user_info_db_json)
other_complete_db = UserAccount(**other_user_complete_user_info_db_json)
user_extra_data_db = UserAccount(**user_info_extra_data_db_json)

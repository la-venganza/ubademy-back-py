import json

from app.models.user import UserAccount

complete_user_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
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
      "blocked": false, \
      "created_courses": [], \
      "enroll_courses": [], \
      "collaborating_courses": [] \
    }'
)

other_user_complete_user_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "filter@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "birth_date": null, \
      "phone_type": null, \
      "phone_number": null, \
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
      "blocked": false, \
      "created_courses": [], \
      "enroll_courses": [], \
      "collaborating_courses": [] \
    }'
)

complete_user_info_expected_json = json.loads(
    '{ \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "birth_date": null, \
      "phone_type": null, \
      "phone_number": null, \
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
      "blocked": false, \
      "created_courses": [], \
      "enroll_courses": [], \
      "collaborating_courses": [] \
    }'
)

basic_user_info_in_json = json.loads(
    '{ \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "user_id": "1", \
      "blocked": false \
    }'
)

basic_user_info_out_json = json.loads(
    '{ \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "birth_date": null, \
      "phone_type": null, \
      "phone_number": null, \
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
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "blocked": false \
    }'
)

user_info_extra_data_db_json = json.loads(
    '{ \
      "id": 1, \
      "username" : "username",  \
      "first_name": "name", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "subscriptions": [ \
        { \
          "active": true, \
          "user_id": "1", \
          "subscription_id": 1, \
          "subscription": { \
            "id": 1, \
            "title": "Free", \
            "price": 0 \
          }, \
          "start_date": "2021-11-21" \
        } \
      ], \
      "user_id": "1", \
      "blocked": false, \
      "created_courses": [], \
      "enroll_courses": [ \
        { \
            "id": 1, \
            "active": true, \
            "start_date": "2020-01-01", \
            "course_id": 1, \
            "course": { \
                "title": "Curso Java", \
                "description": "Venis a aprender", \
                "type": "Programming", \
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
            "id": 1, \
            "creator_id": "1" \
            } \
        } \
      ], \
      "collaborating_courses": [  \
        { \
            "id": 1, \
            "active": true, \
            "start_date": "2020-01-01", \
            "course_id": 1, \
            "course": { \
                  "title": "Curso Java", \
                  "description": "Venis a aprender", \
                  "type": "Programming", \
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
                "id": 1, \
                "creator_id": "1" \
            } \
        } \
      ] \
    }'
)

basic_patch_user_info_json = json.loads(
    '{ \
      "birth_date": "1998-01-20", \
      "first_name": "name patch"\
}'
)

complete_user_patched_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "username" : "username",  \
      "first_name": "name patch", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "is_admin": true, \
      "user_id": "1", \
      "birth_date": "1998-01-20", \
       "subscriptions": [ \
        { \
          "active": true, \
          "end_date": null, \
          "subscription": { \
            "id": 3, \
            "title": "Premium" \
          }, \
          "start_date": "2021-11-21" \
        } \
      ], \
      "blocked": false, \
      "created_courses": [], \
      "enroll_courses": [], \
      "collaborating_courses": [] \
    }'
)

basic_user_patched_info_db_json = json.loads(
    '{ \
      "username" : "username",  \
      "first_name": "name patch", \
      "last_name": "lastname", \
      "email": "some@mail.com.ar", \
      "role": "Owner", \
      "user_id": "1", \
      "is_admin": true, \
      "phone_type": null, \
      "phone_number": null, \
      "birth_date": "1998-01-20", \
      "subscriptions": [ \
        { \
          "active": true, \
          "end_date": null, \
          "subscription": { \
            "id": 3, \
            "title": "Premium" \
          }, \
          "start_date": "2021-11-21" \
        } \
      ], \
      "blocked": false \
    }'
)

user_complete_db = UserAccount(**complete_user_info_db_json)
other_complete_db = UserAccount(**other_user_complete_user_info_db_json)

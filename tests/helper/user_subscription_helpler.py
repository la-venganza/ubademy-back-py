import json

from app.models.subscription import Subscription

user_subscription_info_db_json = json.loads(
    '{ \
      "id": 1, \
      "user_id" : "1",  \
      "subscription_id": 1, \
      "active": true, \
      "start_date": "2021-11-21", \
      "end_date": "2022-11-21", \
       "subscription": { \
            "id": 1, \
            "title": "Free", \
            "price": 0 \
      } \
    }'
)

user_subscription_response_json = json.loads(
    '{ \
      "active": true, \
      "start_date": "2021-11-21", \
      "end_date": "2022-11-21", \
       "subscription": { \
            "id": 1, \
            "title": "Free"\
      } \
    }'
)

user_subscription_inactive_db_json = json.loads(
    '{ \
      "id": 1, \
      "user_id" : "1",  \
      "subscription_id": 2, \
      "active": false, \
      "start_date": "2021-11-21", \
      "end_date": "2022-11-21", \
       "subscription": { \
            "id": 2, \
            "title": "Gold", \
            "price": 10 \
      } \
    }'
)

free_subscription_db_json = json.loads(
    '{ \
        "id": 1, \
        "title": "Free", \
        "price": 0 \
    }'
)

gold_subscription_db_json = json.loads(
    '{ \
        "id": 2, \
        "title": "Gold", \
        "price": 10 \
    }'
)

user_subscription_create_invalid_subscription_json = json.loads(
    '{ \
        "subscription": "Free", \
        "end_date": "2200-10-10" \
    }'
)

user_subscription_create_invalid_end_date_json = json.loads(
    '{ \
        "subscription": "Gold", \
        "end_date": "2010-10-10" \
    }'
)

user_subscription_create_json = json.loads(
    '{ \
        "subscription": "Gold", \
        "end_date": "2100-10-10" \
    }'
)

user_subscription_update_json = json.loads(
    '{ \
        "active": false, \
        "end_date": "2022-10-10" \
    }'
)

gold_subscription_db = Subscription(**gold_subscription_db_json)


import json

from app.crud import user

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

user_complete = UserAccount(**complete_user_info_db_json)
other_complete = UserAccount(**other_user_complete_user_info_db_json)


def test_user_not_found(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.get("/api/v1/users/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_user_ok_basic_info(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete)
    response = test_app.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json() == basic_user_info_json


def test_user_ok_complete_info(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete)
    response = test_app.get("/api/v1/users/1?properties=all")
    assert response.status_code == 200
    assert response.json() == complete_user_info_expected_json


def test_users_invalid_keyword(test_app):
    response = test_app.get("/api/v1/users?keyword=aa")
    assert response.status_code == 422


def test_users_ok_no_users(test_app, mocker):
    mocker.patch.object(user, 'get_multi', return_value=[])
    response = test_app.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_users_ok_with_results(test_app, mocker):
    mocker.patch.object(user, 'get_multi', return_value=[user_complete, user_complete])
    response = test_app.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {'results': [basic_user_info_json, basic_user_info_json]}


def test_users_ok_filter(test_app, mocker):
    mocker.patch.object(user, 'get_multi', return_value=[user_complete, other_complete])
    response = test_app.get("/api/v1/users?keyword=some@mail.com")
    assert response.status_code == 200
    assert response.json() == {'results': [basic_user_info_json]}


def test_users_create_ok(test_app, mocker):
    mocker.patch.object(user, 'get_by_email', return_value=None)
    mocker.patch.object(user, 'create', return_value=user_complete)
    response = test_app.post("/api/v1/users/", data=json.dumps(basic_user_info_json))
    assert response.status_code == 200
    assert response.json() == basic_user_info_json


def test_users_create_already_exists(test_app, mocker):
    mocker.patch.object(user, 'get_by_email', return_value=user_complete)
    response = test_app.post("/api/v1/users/", data=json.dumps(basic_user_info_json))
    assert response.status_code == 200
    assert response.json() == basic_user_info_json

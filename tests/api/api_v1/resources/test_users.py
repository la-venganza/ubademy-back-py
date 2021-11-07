import json

from app.crud import user
from app.models.user import UserAccount
from tests.helper.users_helper import basic_user_info_in_json, complete_user_info_expected_json, \
    other_complete_db, basic_patch_user_info_json, \
    complete_user_patched_info_db_json, basic_user_patched_info_db_json, basic_user_info_out_json

# user_complete_db = UserAccount(**complete_user_info_db_json)
user_patched_complete_db = UserAccount(**complete_user_patched_info_db_json)


# ------------------ User get by id ------------------------ #
def test_user_not_found(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.get("/api/v1/users/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_user_ok_basic_info(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    response = test_app.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json() == basic_user_info_out_json


def test_user_ok_complete_info(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    response = test_app.get("/api/v1/users/1?properties=all")
    assert response.status_code == 200
    assert response.json() == complete_user_info_expected_json


# ------------------ User get users ------------------------ #
def test_users_invalid_keyword(test_app):
    response = test_app.get("/api/v1/users?keyword=aa")
    assert response.status_code == 422


def test_users_ok_no_users(test_app, mocker):
    mocker.patch.object(user, 'get_multi', return_value=[])
    response = test_app.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_users_ok_with_results(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_multi', return_value=[user_complete_db, user_complete_db])
    response = test_app.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {'results': [basic_user_info_out_json, basic_user_info_out_json]}


# ------------------ User get users with filters ------------------------ #
def test_users_ok_filter_keyword(test_app, user_complete_db,  mocker):
    mocker.patch.object(user, 'get_multi', return_value=[user_complete_db, other_complete_db])
    response = test_app.get("/api/v1/users?keyword=some")
    assert response.status_code == 200
    assert response.json() == {'results': [basic_user_info_out_json]}


def test_users_ok_filter_email(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_email', return_value=user_complete_db)
    response = test_app.get("/api/v1/users?email=some@mail.com")
    assert response.status_code == 200
    assert response.json() == {'results': [basic_user_info_out_json]}


# ------------------ User post ------------------------ #
def test_users_create_ok(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_email', return_value=None)
    mocker.patch.object(user, 'create', return_value=user_complete_db)
    response = test_app.post("/api/v1/users/", data=json.dumps(basic_user_info_in_json))
    assert response.status_code == 200
    assert response.json() == basic_user_info_out_json


def test_users_create_already_exists(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_email', return_value=user_complete_db)
    response = test_app.post("/api/v1/users/", data=json.dumps(basic_user_info_in_json))
    assert response.status_code == 200
    assert response.json() == basic_user_info_out_json


# ------------------ User update ------------------------ #
def test_patch_fail_user_not_found(test_app, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=None)
    response = test_app.patch("/api/v1/users/1", data=json.dumps(basic_patch_user_info_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'The user with id 1 was not found'}


def test_patch_user_update_ok(test_app, user_complete_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_complete_db)
    mocker.patch.object(user, 'update', return_value=user_patched_complete_db)
    response = test_app.patch("/api/v1/users/1", data=json.dumps(basic_patch_user_info_json))
    assert response.status_code == 200
    assert response.json() == basic_user_patched_info_db_json

import json

from app.crud import user, user_subscription, subscription
from tests.helper.user_subscription_helpler import user_subscription_create_invalid_subscription_json, \
    user_subscription_create_invalid_end_date_json, user_subscription_create_json, gold_subscription_db, \
    user_subscription_response_json, user_subscription_update_json, user_subscription_premium_response_json


# ------------------ User subscription post ------------------------ #
def test_subscriptions_invalid_subscription(test_app, user_extra_data_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    response = test_app.post("/api/v1/1/subscriptions/",
                             data=json.dumps(user_subscription_create_invalid_subscription_json))
    assert response.status_code == 422


def test_subscriptions_invalid_end_date(test_app, user_extra_data_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    response = test_app.post("/api/v1/1/subscriptions/",
                             data=json.dumps(user_subscription_create_invalid_end_date_json))
    assert response.status_code == 422


def test_subscriptions_create_ok(test_app, user_extra_data_db, user_free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(subscription, 'get_by_subscription_plan', return_value=gold_subscription_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[user_free_subscription_db])
    mocker.patch.object(user_subscription, 'create', return_value=user_free_subscription_db)
    response = test_app.post("/api/v1/1/subscriptions/",
                             data=json.dumps(user_subscription_create_json))
    assert response.status_code == 200
    assert response.json() == user_subscription_response_json


# ------------------ User subscription get for user id ------------------------ #
def test_subscriptions_get_no_filter_no_results(test_app, user_extra_data_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[])
    response = test_app.get("/api/v1/1/subscriptions")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_subscriptions_get_no_filter_results(test_app, user_extra_data_db, user_free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[user_free_subscription_db])
    response = test_app.get("/api/v1/1/subscriptions")
    assert response.status_code == 200
    assert response.json() == {'results': [user_subscription_response_json]}


def test_subscriptions_get_no_filter_results_only_free_active(
        test_app, user_extra_data_db, user_subscriptions_all_db, mocker
):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=user_subscriptions_all_db)
    response = test_app.get("/api/v1/1/subscriptions")
    assert response.status_code == 200
    assert response.json() == {'results': [user_subscription_premium_response_json]}


def test_subscriptions_get_inactive_filter_results(test_app, user_extra_data_db, user_free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[user_free_subscription_db])
    response = test_app.get("/api/v1/1/subscriptions?active_filter=false")
    assert response.status_code == 200
    assert response.json() == {'results': []}


def test_subscriptions_get_active_filter_results(test_app, user_extra_data_db, user_free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[user_free_subscription_db])
    response = test_app.get("/api/v1/1/subscriptions?active_filter=true")
    assert response.status_code == 200
    assert response.json() == {'results': [user_subscription_response_json]}


# ------------------ User subscription patch ------------------------ #
def test_subscriptions_update_invalid_subscription(test_app, user_extra_data_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    response = test_app.patch("/api/v1/1/subscriptions/free",
                              data=json.dumps(user_subscription_update_json))
    assert response.status_code == 422


def test_subscriptions_update_not_found(test_app, user_extra_data_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(subscription, 'get_by_subscription_plan', return_value=gold_subscription_db)
    mocker.patch.object(user_subscription, 'get_subscription_by_user_and_subscription', return_value=None)
    response = test_app.patch("/api/v1/1/subscriptions/gold",
                              data=json.dumps(user_subscription_update_json))
    assert response.status_code == 404
    assert response.json() == {'detail': 'User 1 does not have or had any gold subscription.'}


def test_subscriptions_update_ok(test_app, user_extra_data_db, user_free_subscription_db, mocker):
    mocker.patch.object(user, 'get_by_user_id', return_value=user_extra_data_db)
    mocker.patch.object(subscription, 'get_by_subscription_plan', return_value=gold_subscription_db)
    mocker.patch.object(user_subscription, 'get_subscription_by_user_and_subscription',
                        return_value=user_free_subscription_db)
    mocker.patch.object(user_subscription, 'update', return_value=user_free_subscription_db)

    response = test_app.patch("/api/v1/1/subscriptions/gold",
                              data=json.dumps(user_subscription_update_json))
    assert response.status_code == 200
    assert response.json() == user_subscription_response_json

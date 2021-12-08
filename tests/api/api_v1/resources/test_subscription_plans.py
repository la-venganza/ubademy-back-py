from app.crud import subscription

from app.schemas.subscription import SubscriptionTitle
from tests.helper.user_subscription_helpler import free_subscription_db_json


# ------------------ User subscription plan get by id ------------------------ #
def test_subscription_plan_get_subscription_plans_none(test_app, mocker):
    mocker.patch.object(subscription, 'get_multi', return_value=[])
    response = test_app.get("/api/v1/subscription_plans")
    assert response.status_code == 200
    assert response.json() == {'subscription_plans': []}


def test_subscription_plan_get_subscription_plans_ok(test_app, free_subscription_db, mocker):
    mocker.patch.object(subscription, 'get_multi', return_value=[free_subscription_db])
    response = test_app.get("/api/v1/subscription_plans")
    assert response.status_code == 200
    assert response.json() == {'subscription_plans': [free_subscription_db_json]}


def test_subscription_plan_get_subscription_plan_by_id_not_found(test_app, mocker):
    mocker.patch.object(subscription, 'get', return_value=None)
    response = test_app.get("/api/v1/subscription_plans/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Subscription plan with id 1 does not exist.'}


def test_subscription_plan_get_subscription_plan_by_id_ok(test_app, free_subscription_db, mocker):
    mocker.patch.object(subscription, 'get', return_value=free_subscription_db)
    response = test_app.get("/api/v1/subscription_plans/1")
    assert response.status_code == 200
    assert response.json() == free_subscription_db_json


def test_subscription_title_ignore_case():
    assert SubscriptionTitle["free"] == SubscriptionTitle.free
    assert SubscriptionTitle["Free"] == SubscriptionTitle.free
    assert SubscriptionTitle["FrEe"] == SubscriptionTitle.free

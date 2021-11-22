from datetime import date
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.crud import subscription, user_subscription
from app.services import subscription_service

end_date = date(2025, 12, 31)


@pytest.mark.asyncio
async def test_get_subscription_by_subscription_plan_not_found(mocker):
    mocker.patch.object(subscription, 'get_by_subscription_plan', return_value=None)
    db_session = MagicMock()
    with pytest.raises(HTTPException) as exception_response:
        await subscription_service.get_subscription_by_subscription_plan(subscription_plan_in="Platinum", db=db_session)
    assert exception_response.value.status_code == 404
    assert str(exception_response.value.detail) == 'Subscription with title Platinum was not found'


@pytest.mark.asyncio
async def test_get_subscription_by_subscription_plan_ok(free_subscription_db, mocker):
    mocker.patch.object(subscription, 'get_by_subscription_plan', return_value=free_subscription_db)
    db_session = MagicMock()
    user_db = await subscription_service.get_subscription_by_subscription_plan(
        subscription_plan_in="Free", db=db_session)
    assert user_db == free_subscription_db


@pytest.mark.asyncio
async def test_create_or_update_subscription_for_user_create_ok(user_subscription_db, mocker):
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id', return_value=[user_subscription_db])
    mocker.patch.object(user_subscription, 'create', return_value=user_subscription_db)
    db_session = MagicMock()

    new_user_subscription_db = await subscription_service.create_or_update_subscription_for_user(
            user_id="user_id", subscription_id=2, end_date=end_date, db=db_session)
    assert new_user_subscription_db == user_subscription_db


@pytest.mark.asyncio
async def test_create_or_update_subscription_for_user_more_than_one_subscription(user_subscription_db, mocker):
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id',
                        return_value=[user_subscription_db, user_subscription_db])
    db_session = MagicMock()

    with pytest.raises(HTTPException) as exception_response:
        await subscription_service.create_or_update_subscription_for_user(
            user_id="user_id", subscription_id=1, end_date=end_date, db=db_session)
    assert exception_response.value.status_code == 500
    assert str(exception_response.value.detail) == \
           "There shouldn't be more than 1 same subscription plan type for user. 2 were found for user_id"


@pytest.mark.asyncio
async def test_create_or_update_subscription_for_user_subscription_already_active(user_subscription_db, mocker):
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id',
                        return_value=[user_subscription_db])
    db_session = MagicMock()

    with pytest.raises(HTTPException) as exception_response:
        await subscription_service.create_or_update_subscription_for_user(
            user_id="user_id", subscription_id=1, end_date=end_date, db=db_session)
    assert exception_response.value.status_code == 400
    assert str(exception_response.value.detail) == \
           "Subscription for user user_id already exists and is active until 2022-11-21"


@pytest.mark.asyncio
async def test_create_or_update_subscription_for_user_update_ok(
        user_subscription_db, user_inactive_subscription_db, mocker
):
    mocker.patch.object(user_subscription, 'get_subscriptions_by_user_id',
                        return_value=[user_subscription_db, user_inactive_subscription_db])
    mocker.patch.object(user_subscription, 'update', return_value=user_inactive_subscription_db)
    db_session = MagicMock()

    updated_user_subscription_db = await subscription_service.create_or_update_subscription_for_user(
            user_id="user_id", subscription_id=2, end_date=end_date, db=db_session)
    assert updated_user_subscription_db == user_inactive_subscription_db

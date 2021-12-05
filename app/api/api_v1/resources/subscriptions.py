import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from enum import Enum

from app import deps, crud
from app.services import user_service, subscription_service
from app.models.user import UserAccount
from app.schemas.user_subscription import UserSubscriptionCreateRQ, UserSubscriptionBasics,\
    UserSubscriptionUpdate, UserSubscriptionSearchResults

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=status.HTTP_200_OK, response_model=UserSubscriptionSearchResults)
async def get_user_subscriptions(
        active_filter: Optional[bool] = Query(None, example="false"),
        user: UserAccount = Depends(user_service.get_user_by_id),
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for subscriptions for user
    """
    subscriptions = crud.user_subscription.get_subscriptions_by_user_id(db=db, user_id=user.user_id)
    if active_filter is None:
        current_subscription = subscription_service.get_current_subscription(
            list(filter(lambda subscription: filter_by_active_filter(subscription, True), subscriptions)))
        return {"results": [current_subscription] if current_subscription else []}
    filter_subscriptions = list(filter(lambda subscription:
                                       filter_by_active_filter(subscription, active_filter),
                                       subscriptions))
    return {"results": filter_subscriptions}


def filter_by_active_filter(subscription, active_filter):
    return subscription.active and (not subscription.end_date or subscription.end_date > date.today())\
        if active_filter\
        else (not subscription.active or (subscription.end_date and subscription.end_date < date.today()))


@router_v1.post("/", status_code=status.HTTP_200_OK, response_model=UserSubscriptionBasics)
async def post(
        subscription_in: UserSubscriptionCreateRQ,
        user: UserAccount = Depends(user_service.get_user_by_id),
        db: Session = Depends(deps.get_db),
) -> dict:
    user_id = user.user_id
    subscription_name = subscription_in.subscription
    subscription_plan = await subscription_service.get_subscription_by_subscription_plan(
        db=db, subscription_plan_in=subscription_name)
    logger.info(f"Attempt to subscribe user {user_id} for {subscription_name} subscription.")
    return await subscription_service.create_or_update_subscription_for_user(
        db=db, user_id=user_id, subscription_id=subscription_plan.id, end_date=subscription_in.end_date)


class SubscriptionName(str, Enum):
    gold = "gold"
    premium = "premium"


@router_v1.patch("/{subscription_name}", status_code=status.HTTP_200_OK, response_model=UserSubscriptionBasics)
async def update_user(
        subscription_name: SubscriptionName,
        subscription_in: UserSubscriptionUpdate,
        user=Depends(user_service.get_user_by_id),
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Update user subscription
    """
    subscription_plan = await subscription_service.get_subscription_by_subscription_plan(
        db=db, subscription_plan_in=subscription_name)
    user_subscription = crud.user_subscription.get_subscription_by_user_and_subscription(
        db=db, user_id=user.user_id, subscription_id=subscription_plan.id)
    if not user_subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user.user_id} does not have or had any {subscription_name} subscription.")
    user_subscription_updated = crud.user_subscription.update(
        db=db, db_obj=user_subscription, obj_in=subscription_in)
    return user_subscription_updated

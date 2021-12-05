from datetime import date
from typing import List

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import crud
from app.deps import get_db
from app.schemas.user_subscription import UserSubscriptionCreate, UserSubscriptionUpdate
from app.models.user_subscription import UserSubscription


async def get_subscription_by_subscription_plan(subscription_plan_in: str, db: Session = Depends(get_db)):
    subscription_plan = crud.subscription.get_by_subscription_plan(db=db, subscription_plan=subscription_plan_in)
    if subscription_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Subscription with title {subscription_plan_in} was not found")
    return subscription_plan


async def create_or_update_subscription_for_user(
        user_id: str, subscription_id: int, end_date: date, db: Session = Depends(get_db)):
    subscriptions = crud.user_subscription.get_subscriptions_by_user_id(db=db, user_id=user_id)
    filter_subscription = list(filter(lambda subscription:
                                      subscription_id == subscription.subscription_id, subscriptions))
    if not filter_subscription:
        return crud.user_subscription.create(
            db=db, obj_in=UserSubscriptionCreate(user_id=user_id, subscription_id=subscription_id, end_date=end_date))
    if len(filter_subscription) > 1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"There shouldn't be more than 1 same subscription plan type for user."
                                   f" {len(filter_subscription)} were found for {user_id}")
    db_subscription = filter_subscription[0]
    if db_subscription.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subscription for user {user_id} already exists and is active until {db_subscription.end_date}")
    return crud.user_subscription.update(
        db=db, db_obj=db_subscription, obj_in=UserSubscriptionUpdate(active=True, end_date=end_date))


def get_current_subscription(user_subscriptions: List[UserSubscription]):
    current_subscription = None
    if len(user_subscriptions) == 1:
        current_subscription = user_subscriptions[0]
    current_subscription = find_subscription_by_name(
        user_subscriptions=user_subscriptions, subscription_name="premium")
    if not current_subscription:
        current_subscription = find_subscription_by_name(
            user_subscriptions=user_subscriptions, subscription_name="gold")
    # This should never happen. It should return free in first len scenario
    if not current_subscription:
        current_subscription = find_subscription_by_name(
            user_subscriptions=user_subscriptions, subscription_name="free")
    return current_subscription


def find_subscription_by_name(user_subscriptions: List[UserSubscription], subscription_name: str):
    return next((user_subscription for user_subscription in user_subscriptions if
                 (user_subscription.subscription.title.lower() == subscription_name.lower())), None)

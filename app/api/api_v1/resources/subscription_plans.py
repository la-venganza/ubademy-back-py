from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import deps, crud

from app.schemas.subscription import Subscription, SubscriptionSearchResults


router_v1 = APIRouter()


@router_v1.get("", status_code=status.HTTP_200_OK, response_model=SubscriptionSearchResults)
async def get_subscription_plans(db: Session = Depends(deps.get_db),) -> dict:
    """
    List available subscriptions
    """
    subscriptions = crud.subscription.get_multi(db=db)
    return {"subscription_plans": subscriptions}


@router_v1.get("/{subscription_id}", status_code=status.HTTP_200_OK, response_model=Subscription)
async def get_subscription_plan_by_id(subscription_id: int, db: Session = Depends(deps.get_db),) -> dict:
    """
    Get subscription plan by id
    """
    subscription = crud.subscription.get(db=db, id=subscription_id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription plan with id {subscription_id} does not exist.")
    return subscription

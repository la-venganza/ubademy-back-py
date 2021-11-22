from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.user_subscription import UserSubscription
from app.schemas.user_subscription import UserSubscriptionCreate, UserSubscriptionUpdate
from app.crud.base import CRUDBase


class CRUDSubscription:

    def get_by_subscription_plan(self, db: Session, *, subscription_plan: str) -> Optional[Subscription]:
        return db.query(Subscription).filter(func.lower(Subscription.title) == func.lower(subscription_plan)).first()


subscription = CRUDSubscription()


class CRUDUserSubscription(CRUDBase[UserSubscription, UserSubscriptionCreate, UserSubscriptionUpdate]):

    def get_subscriptions_by_user_id(self, db: Session, *, user_id: str) -> List[UserSubscription]:
        return db.query(UserSubscription).filter(UserSubscription.user_id == user_id).all()

    def get_subscription_by_user_and_subscription(self, db: Session, *, user_id: str,
                                                  subscription_id: int) -> UserSubscription:
        return db.query(UserSubscription).filter(UserSubscription.user_id == user_id,
                                                 UserSubscription.subscription_id == subscription_id).first()


user_subscription = CRUDUserSubscription(UserSubscription)

from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class UserSubscription(Base):
    __tablename__ = 'user_subscription'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey('user_account.user_id'), primary_key=True)
    subscription_id = Column(ForeignKey('subscription.id'), primary_key=True)
    active = Column(Boolean, default=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    subscription = relationship("Subscription")

    @auto_init()
    def __init__(self, **_):
        pass

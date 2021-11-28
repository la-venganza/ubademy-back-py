from datetime import date
from typing import Optional, List

from pydantic import BaseModel, validator

from app.schemas.subscription import SubscriptionBasics


class UserSubscriptionBase(BaseModel):
    active: bool
    end_date: Optional[date] = None


class UserSubscriptionCreateBase(UserSubscriptionBase):
    subscription_id: int
    active: bool = True
    end_date: Optional[date] = None


# Properties to receive via API on creation
class UserSubscriptionCreate(UserSubscriptionCreateBase):
    user_id: str


class UserSubscriptionCreateRQ(BaseModel):
    subscription: str
    end_date: date

    @validator("end_date")
    def validate_end_date(cls, value: date):
        if date.today() < value:
            return value
        raise ValueError('end_date must be a date in the future')

    @validator("subscription")
    def validate_subscription(cls, value: str):
        lower_value = value.lower()
        if lower_value == "gold" or lower_value == "premium":
            return value
        raise ValueError('subscription must be one of the following values: [Gold, Premium]')


class UserSubscriptionInDBBase(UserSubscriptionBase):
    user_id: str
    subscription: SubscriptionBasics
    start_date: date

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserSubscription(UserSubscriptionInDBBase):
    pass


class UserSubscriptionBasics(UserSubscriptionBase):
    subscription: SubscriptionBasics
    start_date: date

    class Config:
        orm_mode = True


class UserSubscriptionSearchResults(BaseModel):
    results: List[UserSubscriptionBasics]


# Properties to receive via API on update
class UserSubscriptionUpdate(UserSubscriptionBase):
    active: Optional[bool]
    end_date: Optional[date]

from typing import List

from aenum import Enum

from pydantic import BaseModel


class SubscriptionTitle(str, Enum):
    free = "Free"
    gold = "Gold"
    premium = "Premium"

    @classmethod
    def _missing_value_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member

    @classmethod
    def _missing_name_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class SubscriptionBase(BaseModel):
    title: SubscriptionTitle
    price: float


class SubscriptionInDBBase(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Subscription(SubscriptionInDBBase):
    price: float


class SubscriptionBasics(SubscriptionInDBBase):
    pass


class SubscriptionSearchResults(BaseModel):
    subscription_plans: List[Subscription]

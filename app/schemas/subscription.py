from enum import Enum

from pydantic import BaseModel


class SubscriptionTitle(str, Enum):
    free = "Free"
    gold = "Gold"
    premium = "Premium"


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

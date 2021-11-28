from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    title: str
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

from sqlalchemy import Column, Integer, String, Float

from app.db.base_class import Base, auto_init


class Subscription(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)

    @auto_init()
    def __init__(self, **_):
        pass

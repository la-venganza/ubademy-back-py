from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class UserAccount(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(256), unique=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    role = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)

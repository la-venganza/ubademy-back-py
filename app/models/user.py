from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init
from app.models.collaborator import collaborator_table


class UserAccount(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(256), unique=True, index=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone_type = Column(String(20), nullable=True)
    phone_number = Column(String(30), nullable=True)
    email = Column(String, index=True, nullable=False)
    role = Column(String, nullable=True)
    subscription = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    blocked = Column(Boolean, default=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    created_courses = relationship(
        "Course",
        cascade="all,delete-orphan",
        back_populates="creator",
        uselist=True,
    )
    enroll_courses = relationship("EnrollCourse", back_populates="user")
    collaborating_courses = relationship(
        "Course",
        secondary=collaborator_table,
        back_populates="collaborators")

    @auto_init()
    def __init__(self, **_):
        pass

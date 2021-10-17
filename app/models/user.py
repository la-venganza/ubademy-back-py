from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.student import student_table
from app.models.collaborator import collaborator_table


class UserAccount(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(256), unique=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    role = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_courses = relationship(
        "Course",
        cascade="all,delete-orphan",
        back_populates="creator",
        uselist=True,
    )
    attending_courses = relationship(
        "Course",
        secondary=student_table,
        back_populates="students")
    collaborating_courses = relationship(
        "Course",
        secondary=collaborator_table,
        back_populates="collaborators")

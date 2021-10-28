from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.student import student_table
from app.models.collaborator import collaborator_table


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(String(256), nullable=True)
    type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=True)
    hashtags = Column(String(256), index=True, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    creator_id = Column(String(256), ForeignKey("user_account.user_id"), nullable=True)
    creator = relationship("UserAccount", back_populates="created_courses")
    students = relationship(
        "UserAccount",
        secondary=student_table,
        back_populates="attending_courses")
    collaborators = relationship(
        "UserAccount",
        secondary=collaborator_table,
        back_populates="collaborating_courses"
    )
    lessons = relationship("Lesson")

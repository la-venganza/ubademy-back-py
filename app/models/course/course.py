from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


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
    enrollments = relationship("EnrollCourse", back_populates="course")
    collaborators = relationship("Collaborator", back_populates="course")
    lessons = relationship(
        "Lesson",
        cascade="all, delete",
        passive_deletes=True
    )

    @auto_init()
    def __init__(self, **_):
        pass

from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class EnrollCourse(Base):
    __tablename__ = 'enroll_course'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey('user_account.user_id'), primary_key=True)
    course_id = Column(ForeignKey('course.id'), primary_key=True)
    active = Column(Boolean, default=True)
    current_lesson = Column(Integer, nullable=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    grade = Column(Integer, nullable=True)
    course = relationship("Course", back_populates="enrollments")
    user = relationship("UserAccount", back_populates="enroll_courses")

    @auto_init()
    def __init__(self, **_):
        pass

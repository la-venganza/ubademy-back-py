from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class EnrollCourseExam(Base):
    __tablename__ = 'enroll_course_exam'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    enroll_course_id = Column(ForeignKey('enroll_course.id'), primary_key=True)
    lesson_id = Column(ForeignKey('lesson.id'), primary_key=True)
    exam_id = Column(ForeignKey('exam.id'), primary_key=True)
    exam_date = Column(DateTime(timezone=True), server_default=func.now())
    grade = Column(Integer, nullable=True)
    enroll_course = relationship("EnrollCourse", back_populates="exams")
    exams = relationship("Exam")
    answers = relationship("Answer")

    @auto_init()
    def __init__(self, **_):
        pass

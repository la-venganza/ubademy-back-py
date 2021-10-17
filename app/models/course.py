from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.student import student_table


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    length = Column(String(256), nullable=False)
    year = Column(Integer, nullable=False)
    teacher = Column(String(256), nullable=False)
    subject = Column(String(256), index=True, nullable=False)
    creator_id = Column(String(256), ForeignKey("user_account.user_id"), nullable=True)
    creator = relationship("UserAccount", back_populates="created_courses")
    students = relationship(
        "UserAccount",
        secondary=student_table,
        back_populates="attending_courses")

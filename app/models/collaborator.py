from sqlalchemy import Column, ForeignKey, Integer, Boolean, Date, func, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base, auto_init


class Collaborator(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(ForeignKey('user_account.user_id'), primary_key=True)
    course_id = Column(ForeignKey('course.id'), primary_key=True)
    active = Column(Boolean, default=True)
    start_date = Column(Date, server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    course = relationship("Course", back_populates="collaborators")
    user = relationship("UserAccount", back_populates="collaborating_courses")

    @auto_init()
    def __init__(self, **_):
        pass

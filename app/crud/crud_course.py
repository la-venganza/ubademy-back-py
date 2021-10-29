from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.course.course import Course
from app.schemas.course.course import CourseCreate, CourseUpdate


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):

    def get_full_by_course_id(self, db: Session, *, course_id: str) -> Optional[Course]:
        return db.query(Course).options(joinedload('*')).filter(Course.id == course_id).first()

    ...


course = CRUDCourse(Course)

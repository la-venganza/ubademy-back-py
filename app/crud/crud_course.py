from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.course.course import Course
from app.schemas.course.course import CourseCreate, CourseUpdate, Course as CoursePydantic


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):

    def get_full_by_course_id(self, db: Session, *, course_id: str) -> Optional[Course]:
        return db.query(Course).options(joinedload('*')).filter(Course.id == course_id).first()

    def patch_course(
        self,
        db: Session,
        *,
        course_to_update: CourseUpdate,
        course_db_data: Course
    ) -> Course:
        pydantic_course_stored = CoursePydantic.from_orm(course_db_data)

        course_updates_data = course_to_update.dict(exclude_unset=True)

        # create the merged dict with new updates overwriting existing data
        updated_course_data = pydantic_course_stored.copy(update=course_updates_data)

        course_to_update_data = jsonable_encoder(updated_course_data, by_alias=False)
        course_to_update_db = self.model(**course_to_update_data)  # type: ignore
        db.merge(course_to_update_db)
        db.commit()
        db.refresh(course_db_data)
        return course_db_data

    ...


course = CRUDCourse(Course)

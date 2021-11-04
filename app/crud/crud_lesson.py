from app.crud.base import CRUDBase

from sqlalchemy.orm import Session

from app.models.course.lesson import Lesson
from app.schemas.course.lesson import LessonCreate, LessonUpdate


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):

    def update_lesson(self, db: Session, *, updated_lesson: Lesson) -> Lesson:
        db.add(updated_lesson)
        db.commit()
        db.refresh(updated_lesson)
        return updated_lesson

    ...


lesson = CRUDLesson(Lesson)

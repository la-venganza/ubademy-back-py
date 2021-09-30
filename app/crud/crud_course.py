from app.crud.base import CRUDBase
from app.courses.models import Course
from app.courses.schemas import CourseCreate, CourseUpdate


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    ...


course = CRUDCourse(Course)

from app.crud.base import CRUDBase

from app.models.enroll_course import EnrollCourse
from app.schemas.enroll_course import EnrollCourseCreate, EnrollCourseUpdate


class CRUDEnrollCourse(CRUDBase[EnrollCourse, EnrollCourseCreate, EnrollCourseUpdate]):
    ...


enroll_course = CRUDEnrollCourse(EnrollCourse)

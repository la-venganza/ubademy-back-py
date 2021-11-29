from app.crud.base import CRUDBase

from app.models.enroll_course_exam import EnrollCourseExam
from app.schemas.enroll_course_exam import EnrollCourseExamCreate, EnrollCourseExamUpdate


class CRUDEnrollCourseExam(CRUDBase[EnrollCourseExam, EnrollCourseExamCreate, EnrollCourseExamUpdate]):
    ...


enroll_course_exam = CRUDEnrollCourseExam(EnrollCourseExam)

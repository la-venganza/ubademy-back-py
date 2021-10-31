from app.crud.base import CRUDBase
from app.models.course.exam import Exam
from app.schemas.course.exam import ExamCreate, ExamUpdate


class CRUDExam(CRUDBase[Exam, ExamCreate, ExamUpdate]):
    ...


course = CRUDExam(Exam)

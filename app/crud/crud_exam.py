from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.course.exam import Exam
from app.schemas.course.exam import ExamCreate, ExamUpdate, Exam as ExamPydantic


class CRUDExam(CRUDBase[Exam, ExamCreate, ExamUpdate]):

    def patch_exam(
        self,
        db: Session,
        *,
        exam_to_update: ExamUpdate,
        exam_db_data: Exam
    ) -> Exam:
        pydantic_exam_stored = ExamPydantic.from_orm(exam_db_data)

        exam_updates_data = exam_to_update.dict(exclude_unset=True)

        # create the merged dict with new updates overwriting existing data
        updated_exam_data = pydantic_exam_stored.copy(update=exam_updates_data)

        exam_to_update_data = jsonable_encoder(updated_exam_data, by_alias=False)
        exam_to_update_db = self.model(**exam_to_update_data)  # type: ignore
        db.merge(exam_to_update_db)
        db.commit()
        db.refresh(exam_db_data)
        return exam_db_data

    ...


exam = CRUDExam(Exam)

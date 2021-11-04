from unittest.mock import MagicMock

from app.crud import exam
from app.schemas.course.exam import ExamUpdate
from tests.helper.exams_helper import exam_patch_json, exam_db

exam_patch = ExamUpdate(**exam_patch_json)


def test_crud_exam_patch():
    db_session = MagicMock()

    exam.patch_exam(db=db_session, exam_to_update=exam_patch, exam_db_data=exam_db)

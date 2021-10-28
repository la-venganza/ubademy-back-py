from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.course.course import Course
from app.schemas.course.course import CourseCreate, CourseUpdate
from app.models.course import Lesson, Exam
from models.course import Question, Choice, DevelopQuestion, MultipleChoiceQuestion


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):

    def get_full_by_course_id(self, db: Session, *, course_id: str) -> Optional[Course]:
        return db.query(Course).options(joinedload('*')).filter(Course.id == course_id).first()

    # Insane: https://stackoverflow.com/questions/61144192/insert-a-nested-schema-into-a-database-with-fastapi
    def create_course(self, db: Session, *, course_in: CourseCreate) -> Course:
        # split information
        course_data = jsonable_encoder(course_in, by_alias=False)
        lessons_data = course_data.pop('lessons', None)

        course_model = Course(**course_data)
        for lesson_data in lessons_data:
            lesson_model = Lesson(**lesson_data)
            course_model.lessons.append(lesson_model)
            exam_data = lesson_data.pop('exam', None)
            if exam_data:
                questions_data = exam_data.pop('questions', None)
                exam_model = Exam(**exam_data)
                lesson_model.exam = exam_model
                for question_data in questions_data:
                    multiple_choice_question_data = question_data.pop('multiple_choice_question', None)
                    develop_question_data = question_data.pop('develop_question', None)
                    question_model = Question(**question_data)
                    exam_model.questions.append(question_model)
                    if multiple_choice_question_data:
                        choices_data = multiple_choice_question_data.pop('choices', None)
                        multiple_choice_question_model = MultipleChoiceQuestion(**multiple_choice_question_data)
                        question_model.multiple_choice_question = multiple_choice_question_model
                        for choice_data in choices_data:
                            choice_model = Choice(**choice_data)
                            question_model.multiple_choice_question.choices.append(choice_model)
                    if develop_question_data:
                        develop_question_model = DevelopQuestion(**develop_question_data)
                        question_model.develop_question = develop_question_model

        db.add(course_model)
        db.commit()
        db.refresh(course_model)
        return course_model

    ...


course = CRUDCourse(Course)

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import UserAccount  # noqa
from app.models.enroll_course import EnrollCourse  # noqa
from app.models.collaborator import collaborator_table  # noqa
from app.models.course.course import Course  # noqa
from app.models.course.lesson import Lesson  # noqa
from app.models.course.exam import Exam  # noqa
from app.models.course.question import Question  # noqa
from app.models.course.multiple_choice_question import MultipleChoiceQuestion  # noqa
from app.models.course.develop_question import DevelopQuestion  # noqa
from app.models.course.choice import Choice  # noqa

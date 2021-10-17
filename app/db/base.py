# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import UserAccount  # noqa
from app.models.course import Course  # noqa
from app.models.student import student_table  # noqa
from app.models.collaborator import collaborator_table  # noqa

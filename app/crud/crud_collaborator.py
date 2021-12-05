from app.crud.base import CRUDBase

from app.models.collaborator import Collaborator
from app.schemas.collaborator import CollaboratorCreate, CollaboratorUpdate


class CRUDCollaborator(CRUDBase[Collaborator, CollaboratorCreate, CollaboratorUpdate]):
    ...


collaborator = CRUDCollaborator(Collaborator)

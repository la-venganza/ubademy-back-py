import uuid
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import UserAccount
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[UserAccount, UserCreate, UserUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[UserAccount]:
        return db.query(UserAccount).filter(UserAccount.user_id == user_id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserAccount]:
        return db.query(UserAccount).filter(func.lower(UserAccount.email) == func.lower(email)).first()

    def get_users_with_filters(self, db: Session, *, email_contains_filer: str,
                               offset: int = 0, limit: int = 100) -> List[UserAccount]:
        query = db.query(UserAccount)
        if email_contains_filer is not None:
            email_contains = '%{0}%'.format(email_contains_filer)
            query = query.filter(UserAccount.email.ilike(email_contains))
        return query.offset(offset).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> UserAccount:
        create_data = obj_in.dict()
        db_obj = UserAccount(**create_data)
        user_id = str(uuid.uuid4())
        db_obj.user_id = user_id
        db.add(db_obj)
        db.commit()

        return db_obj

    def updated_user(self, db: Session, *, updated_user: UserAccount) -> UserAccount:
        db.add(updated_user)
        db.commit()
        db.refresh(updated_user)
        return updated_user

    def update(
        self, db: Session, *, db_obj: UserAccount, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserAccount:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_admin(self, user: UserAccount) -> bool:
        return user.is_admin


user = CRUDUser(UserAccount)

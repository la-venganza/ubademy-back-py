from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud


async def get_user_by_id(db: Session, user_id):
    user = crud.user.get_by_user_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")
    return user

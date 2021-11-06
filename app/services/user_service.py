from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import crud
from app.deps import get_db


async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = crud.user.get_by_user_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")
    return user

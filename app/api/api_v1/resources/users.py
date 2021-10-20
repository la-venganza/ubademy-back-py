import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User, UserSearchResults, UserInDBCompleteBase
from app import deps
from app import crud


logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=status.HTTP_200_OK, response_model=UserSearchResults)
async def get_users(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="someone@someone.com"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for users based on email keyword
    """
    users = crud.user.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": users}

    results = filter(lambda user: keyword.lower() in user.email.lower(), users)
    return {"results": list(results)[:max_results]}


@router_v1.post("/", status_code=status.HTTP_200_OK, response_model=User)
async def post(user_in: UserCreate, db: Session = Depends(deps.get_db),) -> dict:
    email = user_in.email
    logger.info(f"Attempt to create new user for {email}")
    existent_user = crud.user.get_by_email(db=db, email=email)
    if existent_user:
        logger.info(f"User with email {email} already exist.")
        return existent_user
    logger.info(f"User created for email {email}")
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router_v1.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Union[UserInDBCompleteBase, User])
async def get(
        user_id: str,
        db: Session = Depends(deps.get_db),
        properties: Optional[str] = Query(None, min_length=3, example="all"),
        ):
    """""
    Get a single basic user by id, if property all is sent, full information is get.
    """
    user = crud.user.get_by_user_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user with id {user_id} was not found")

    if "all" == properties:
        return UserInDBCompleteBase.from_orm(user)

    return User.from_orm(user)

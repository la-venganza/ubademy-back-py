import logging
from typing import Optional, Union

from fastapi import APIRouter, Depends, Query, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.schemas.user import UserCreateRQ, UserCreate, User, UserSearchResults, UserInDBCompleteBase, UserUpdate
from app import deps, crud
from app.services import user_service, subscription_service
from app.models.user import UserAccount
from app.schemas.user_subscription import UserSubscriptionCreateBase

logger = logging.getLogger(__name__)

router_v1 = APIRouter()


@router_v1.get("/", status_code=status.HTTP_200_OK, response_model=UserSearchResults)
async def get_users(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="gmail"),
        email: Optional[EmailStr] = Query(None, example="someone@someone.com"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for users based on email or/and email information
    """
    if email:
        user = crud.user.get_by_email(db=db, email=email)
        response = [user] if user else []
        return {"results": response}

    users = crud.user.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": users}

    results = filter(lambda user: keyword.lower() in user.email.lower(), users)
    return {"results": list(results)[:max_results]}


def basic_user_to_create(user_in: UserCreateRQ, base_subscription):
    subscription = UserSubscriptionCreateBase(subscription_id=base_subscription.id)
    return UserCreate(username=user_in.username, email=user_in.email, first_name=user_in.first_name,
                      last_name=user_in.last_name, role=user_in.role, birth_date=user_in.birth_date,
                      phone_type=user_in.phone_type, phone_number=user_in.phone_number,
                      subscriptions=[subscription])


@router_v1.post("/", status_code=status.HTTP_200_OK, response_model=User)
async def post(user_in: UserCreateRQ, db: Session = Depends(deps.get_db), ) -> dict:
    email = user_in.email
    logger.info(f"Attempt to create new user for {email}")
    existent_user = crud.user.get_by_email(db=db, email=email)
    if existent_user:
        logger.info(f"User with email {email} already exist.")
        return existent_user
    logger.info(f"User created for email {email}")

    base_subscription = await subscription_service.get_subscription_by_subscription_plan(db=db,
                                                                                         subscription_plan_in="Free")
    user_to_create = basic_user_to_create(user_in, base_subscription)
    user = crud.user.create(db=db, obj_in=user_to_create)
    return user


@router_v1.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Union[UserInDBCompleteBase, User])
async def get(
        user_id: str,
        db: Session = Depends(deps.get_db),
        properties: Optional[str] = Query(None, min_length=3, example="all"),
):
    """
    Get a single basic user by id, if property all is sent, full information is get.
    """
    user = await user_service.get_user_by_id(db=db, user_id=user_id)

    if "all" == properties:
        return UserInDBCompleteBase.from_orm(user)

    return User.from_orm(user)


@router_v1.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_update_rq: UserUpdate, user: UserAccount = Depends(user_service.get_user_by_id),
                      db: Session = Depends(deps.get_db), ) -> dict:
    """
    Update user profile information
    """
    user_updated = crud.user.update(db=db, db_obj=user, obj_in=user_update_rq)
    return user_updated

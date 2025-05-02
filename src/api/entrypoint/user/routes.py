from fastapi import APIRouter, Request, Depends
from typing import Annotated
from src.db_schemas.user import Users
from src.core.extensions import get_db_session
from src.api.entrypoint.user import models
from src.modules.auth.handlers import get_current_user
from src.modules.user.handlers import check_user_member_type
from src.modules.user.handlers import get_users, get_user_by_id
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
# later add param for page_number and page_size
async def list_user_resource(
    request: Request,
    current_user: Annotated[Users, Depends(get_current_user)],
    db_session: Session = Depends(get_db_session),
):
    check_user_member_type(current_user, "admin")
    users = get_users(db_session)
    return users


@router.get("/{user_id}")
# later add param for page_number and page_size
async def get_user_resource(
    request: Request,
    user_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
    db_session: Session = Depends(get_db_session),
):
    check_user_member_type(current_user, "admin")
    users = get_user_by_id(db_session, user_id)
    return users


# @router.patch("/{user_id}")
# async def update_user_details(request: Request,username:str): ...

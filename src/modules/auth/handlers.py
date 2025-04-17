import jwt
from src.core.log_config import logger
from src.modules.auth.exceptions import (
    DuplicateUserException,
    FailedToSaveUserException,
    InvalidTokenException,
)
from src.modules.auth.queries import save_user_to_db
from src.modules.user.queries import get_user_from_db_by_username
from src.api.entrypoint.auth.models import UserRegisterModel, TokenData
from src.api.entrypoint.auth.responses import UserRegisterResponse
from datetime import datetime, timezone, timedelta
from src.core.dependencies import oauth2_scheme
from fastapi import Depends
from typing import Annotated
from src.modules.user.exceptions import UserNotFoundException
from src.db_schemas.user import Users
from src.config.settings import DefaultSettings,get_default_settings
from src.core.extensions import get_db_session
from sqlalchemy.orm import Session

def check_duplicate_user(db_session, username):
    # breakpoint()
    user = get_user_from_db_by_username(db_session, username)
    # breakpoint()
    if user:
        logger.warning("Trying to create duplicate user")
        raise DuplicateUserException(f"User with username {username} already exists")
    else:
        return None


def persist_user_to_db(db_session, model: UserRegisterModel):
    # breakpoint()
    data = Users(**model.model_dump())
    user: Users = save_user_to_db(db_session, data)
    if not user:
        logger.error("Failed to save user in database")
        db_session.rollback()
        raise FailedToSaveUserException(
            f"An Unexpected error occured while creating user with username {data.username}"
        )
    # breakpoint()
    user_dict = user.__dict__
    # return UserRegisterResponse(**vars(user))
    return UserRegisterResponse(**user_dict)


def create_access_token(data: dict, default: DefaultSettings):
    expires_delta: timedelta | None = default.access_token_expire_minutes
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, default.secret, algorithm=default.algorithm)
    return encoded_jwt


def get_current_user(
    db_session: Annotated[Session, Depends(get_db_session)],
    default: Annotated[DefaultSettings,Depends(get_default_settings)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(token, default.secret, algorithms=[default.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenException("Invalid Token")
            # raise UserNotFoundException("User Not Found")
            # return JSONResponse(status_code=404,content={'detail':"username not found"})
        token_data = TokenData(username=username)

    except Exception:
        raise InvalidTokenException("Invalid Token")
    user = get_user_from_db_by_username(db_session, token_data.username)

    if not user:
        raise UserNotFoundException("Could not validate Credentials")
        # return JSONResponse(status_code=401,content={'detail':'Could not validate Credentials'})
    return user

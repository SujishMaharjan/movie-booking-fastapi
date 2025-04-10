import jwt
from src.core.log_config import logger
from src.modules.auth.exceptions import DuplicateUserException, FailedToSaveUserException
from src.modules.auth.queries import save_user_to_db
from src.modules.user.queries import get_user_from_db_by_username
from src.api.entrypoint.auth.models import UserRegisterModel,TokenData
from src.api.entrypoint.auth.responses import UserRegisterResponse
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from src.core.config import SECRET_KEY, ALGORITHM, oauth2_scheme
from fastapi import Depends
from typing import Annotated
from src.core.extensions import db_dependency
from src.modules.auth.exceptions import  InvalidTokenException
from src.modules.user.exceptions import  UserNotFoundException
from src.db_schemas.user import Users



def check_duplicate_user(db,username):
    # breakpoint()
    user = get_user_from_db_by_username(db,username)
    # breakpoint()
    if user:
        logger.warning("Trying to create duplicate user")
        raise DuplicateUserException(
            f"User with username {username} already exists"
        )
    else:
        return None
        



def persist_user_to_db(db,model: UserRegisterModel):
    # breakpoint()
    data = Users(**model.model_dump())
    user: Users = save_user_to_db(db,data)
    if not user:
         logger.error("Failed to save user in database")
         db.rollback()
         raise FailedToSaveUserException(
              f"An Unexpected error occured while creating user with username {data.username}"
         )
    # breakpoint()
    user_dict = user.__dict__
    # return UserRegisterResponse(**vars(user))
    return UserRegisterResponse(**user_dict)





def create_access_token(data: dict,ALGORITHM,SECRET_KEY,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db:db_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username :str = payload.get('sub')
        if username is None:
            raise InvalidTokenException("Invalid Token")
            # raise UserNotFoundException("User Not Found")
            # return JSONResponse(status_code=404,content={'detail':"username not found"})
        token_data = TokenData(username=username)
        
    except Exception:
        raise InvalidTokenException("Invalid Token")
    user = get_user_from_db_by_username(db,token_data.username)

    if not user:
        raise UserNotFoundException
        return JSONResponse(status_code=401,content={'detail':'Could not validate Credentials'})
    return user

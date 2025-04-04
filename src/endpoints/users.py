from fastapi import APIRouter,Depends
from ..log import logger
from ..model.user import UsersBase
from ..handlers.user_handler import create_user
from ..dependencies import db_dependency
from fastapi.security import  OAuth2PasswordRequestForm
from ..auth.auth import authenticate_user
from ..exceptions import InvalidUserNamePasswordError,UserCreationError
from fastapi.security import OAuth2PasswordBearer









router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_users(user: UsersBase, db:db_dependency):
    logger.info("users endpoint accessed")

    user_response = create_user(db,user)
    if not user_response:
        raise UserCreationError
    
    return user_response


@router.post('/login/',tags=["users"]) 
def login_user( db:db_dependency,form_data: OAuth2PasswordRequestForm=Depends()):
    logger.info("login endpoint accessed")

    token = authenticate_user(db,form_data.username,form_data.password)
    if not token:
        raise InvalidUserNamePasswordError
    
    logger.info(f"{form_data.username} logged in")
    return token

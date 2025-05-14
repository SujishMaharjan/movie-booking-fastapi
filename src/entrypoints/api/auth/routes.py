from fastapi import APIRouter, Request, Depends,Form
from src.core.database import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.entrypoints.api.auth.models import UserRegisterModel
from src.modules.auth.application.register_user import RegisterUser
from src.modules.auth.application.login_user import LoginUser
from src.entrypoints.api.auth.responses import UserRegisterResponse,TokenResponse
from src.core.dependencies import AnnotatedRepositoryProvider
from src.core.log_config import logger
from src.core.exceptions import UnauthorizedException



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def register_user(
    request: Request,
    model: Annotated[UserRegisterModel,Form()],
    provider: AnnotatedRepositoryProvider

):
    logger.info("Signup request received for username: %s", model.username)
    new_user = RegisterUser(provider).execute(model.name, model.username, model.password.get_secret_value(), model.phone, model.email,)
    return UserRegisterResponse(**vars(new_user))
    
@router.post("/signin")
async def login_user(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    form_data: OAuth2PasswordRequestForm = Depends(),  
):  
    
    logger.info("Sign in attempt for username: %s", form_data.username)
    access_token = LoginUser(provider).execute(form_data.username,form_data.password)
    logger.info("User logged in Successfylly : %s", form_data.username)
    return TokenResponse(access_token=access_token, token_type="bearer")
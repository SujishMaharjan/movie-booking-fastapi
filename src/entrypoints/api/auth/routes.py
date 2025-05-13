from fastapi import APIRouter, Request, Depends,Form
from src.core.database import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from src.modules.auth.infrastructure import (
    bycrypt_password_hasher,
    Jwt_token_repository
)
from src.entrypoints.api.auth.models import UserRegisterModel
from src.modules.auth.application.register_user import RegisterUser
from src.modules.auth.application.login_user import LoginUser
from src.entrypoints.api.auth.responses import UserRegisterResponse,TokenResponse
from src.core.dependencies import AnnotatedJwtSettings
from src.modules.user.infrastructure import user_postgres_repository
from src.core.dependencies import AnnotatedRepositoryProvider



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def register_user(
    request: Request,
    model: Annotated[UserRegisterModel,Form()],
    provider: AnnotatedRepositoryProvider

):
    
    new_user = RegisterUser(provider).execute(model.name, model.username, model.password.get_secret_value(), model.phone, model.email,)
    return UserRegisterResponse(**new_user.__dict__)


@router.post("/signin")
async def login_user(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    form_data: OAuth2PasswordRequestForm = Depends(),  
):

    access_token = LoginUser(provider).execute(form_data.username,form_data.password)
    return TokenResponse(access_token=access_token, token_type="bearer")

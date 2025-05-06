from fastapi import APIRouter, Request, Depends,Form
from src.core.infrastucture.persistence.database_postgres import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from src.modules.auth.infrastructure import (
    bycrypt_password_hasher,
    Jwt_token_repository,
    user_postgres_repository
)
from src.api.entrypoint.auth.models import UserRegisterModel
from src.modules.auth.application.register_user import RegisterUser
from src.modules.auth.application.login_user import LoginUser
from src.api.entrypoint.auth.responses import UserRegisterResponse,TokenResponse
from src.core.dependencies import AnnotatedJwtSettings



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def register_user(
    request: Request,
    model: Annotated[UserRegisterModel,Form()],
    db_session: Session = Depends(get_db_session),
):
    user_repo = user_postgres_repository.PostgresUserRepository(db_session)
    hash_repo = bycrypt_password_hasher.BcryptPasswordHasher()
    new_user = RegisterUser(user_repo,hash_repo).execute(model.name, model.username, model.password.get_secret_value(), model.phone, model.email, model.role)
    return UserRegisterResponse(**new_user)


@router.post("/signin")
async def login_user(
    request: Request,
    jwt_settings: AnnotatedJwtSettings,
    db_session: Session = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(),  
):
    user_repo = user_postgres_repository.PostgresUserRepository(db_session)
    hash_repo = bycrypt_password_hasher.BcryptPasswordHasher()
    token_repo = Jwt_token_repository.JwtToken(jwt_settings)

    access_token = LoginUser(user_repo,hash_repo,token_repo).execute(form_data.username,form_data.password)
    return TokenResponse(access_token=access_token, token_type="bearer")

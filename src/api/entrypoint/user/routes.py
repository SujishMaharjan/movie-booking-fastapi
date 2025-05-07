from fastapi import APIRouter, Request, Depends
from typing import Annotated
from src.core.infrastucture.persistence.database_postgres import get_db_session
from sqlalchemy.orm import Session
from src.core.dependencies import oauth2_scheme,AnnotatedJwtSettings
from src.modules.auth.infrastructure import (
    Jwt_token_repository
)
from src.modules.user.application import list_users,get_user,get_user_own
from src.modules.user.infrastructure import user_postgres_repository
from src.api.entrypoint.user.responses import AllUserResponse,UserIdResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
# later add param for page_number and page_size
async def list_user_resource(
    request: Request,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    user_repo = user_postgres_repository.PostgresUserRepository(db_session)
    token_repo = Jwt_token_repository.JwtToken(jwt_settings)
    users = list_users.ListUser(token,user_repo,token_repo).execute()
    return [AllUserResponse(**user.__dict__) for user in users]
    

@router.get("/{user_id}")
async def get_user_resource(
    request: Request,
    user_id: str,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    user_repo = user_postgres_repository.PostgresUserRepository(db_session)
    token_repo = Jwt_token_repository.JwtToken(jwt_settings)
    user = get_user.GetUser(token,user_repo,token_repo).execute(user_id)
    return UserIdResponse(**user.__dict__)

@router.get("/me")
async def get_user_resource(
    request: Request,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    user_repo = user_postgres_repository.PostgresUserRepository(db_session)
    token_repo = Jwt_token_repository.JwtToken(jwt_settings)
    user = get_user_own.GetUserOwn(token,user_repo,token_repo).execute()
    return UserIdResponse(**user.__dict__)

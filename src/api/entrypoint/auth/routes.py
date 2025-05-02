from fastapi import APIRouter, Request, Depends,Form
from src.api.entrypoint.auth import models
from src.modules.auth.handlers import (
    check_duplicate_user,
    persist_user_to_db,
    get_user_from_db_by_username,
)
from src.core.extensions import get_db_session
from src.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from src.modules.user.handlers import get_user
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def register_user(
    request: Request,
    model: Annotated[models.UserRegisterModel,Form()],
    db_session: Session = Depends(get_db_session),
):
    check_duplicate_user(db_session, model.username)
    model.password = str(hash_password(model.password.get_secret_value()))
    user = persist_user_to_db(db_session, model)
    return user


@router.post("/signin")
async def login_user(
    request: Request,
    db_session: Session = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    user = get_user(db_session, form_data.username)
    verify_password(form_data.password, user.password)
    access_token = create_access_token(
        {"sub": user.username}, request.app.state.settings.default
    )
    return models.Token(access_token=access_token, token_type="bearer")

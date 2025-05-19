from fastapi import APIRouter, Request, Depends, Form
from typing import Annotated
from src.entrypoints.api.auth.models import UserRegisterModel,LoginFormData
from src.modules.auth.application.register_user import register_user_service
from src.modules.auth.application.login_user import login_user_service
from src.entrypoints.api.auth.responses import UserRegisterResponse, TokenResponse
from src.core.dependencies import AnnotatedRepositoryProvider
from src.core.log_config import logger
from src.core.exceptions import UnauthorizedException


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def register_user(
    request: Request,
    model: Annotated[UserRegisterModel, Form()],
    provider: AnnotatedRepositoryProvider,
):
    logger.info("Signup request received for username: %s", model.username)
    new_user = register_user_service(
        model.name,
        model.username,
        model.password.get_secret_value(),
        model.phone,
        model.email,
        provider
    )
    return UserRegisterResponse(**vars(new_user))


@router.post("/signin")
async def login_user(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    form_data: Annotated[LoginFormData,Form()],
):

    logger.info("Sign in attempt for username: %s", form_data.username)
    access_token = login_user_service(
        form_data.username,
        form_data.password.get_secret_value(),
        provider
    )
    logger.info("User logged in Successfylly : %s", form_data.username)
    return TokenResponse(access_token=access_token, token_type="bearer")

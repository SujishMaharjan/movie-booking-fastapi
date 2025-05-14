
from typing import Annotated
from src.config.settings import JwtSettings,HallSettings
from fastapi import Depends,Request
from src.core.provider import Provider
from src.modules.user.entity.user import User
from src.core.security import get_current_user


def get_jwt_settings(request: Request):
    return request.app.state.settings.jwt

def get_hall_settings(request: Request):
    return request.app.state.settings.hall

def get_provider(request: Request)->Provider:
    return Provider(request)




AnnotatedCurrentUser = Annotated[User,Depends(get_current_user)]
AnnotatedRepositoryProvider = Annotated[Provider,Depends(get_provider)]
AnnotatedJwtSettings = Annotated[JwtSettings,Depends(get_jwt_settings)]
AnnotatedHallSettings = Annotated[HallSettings,Depends(get_hall_settings)]


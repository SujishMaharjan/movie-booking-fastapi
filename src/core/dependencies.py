from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.config.settings import JwtSettings,HallSettings
from fastapi import Depends,Request



def get_jwt_settings(request: Request):
    return request.app.state.settings.jwt

def get_hall_settings(request: Request):
    return request.app.state.settings.hall


AnnotatedJwtSettings = Annotated[JwtSettings,Depends(get_jwt_settings)]
AnnotatedHallSettings = Annotated[HallSettings,Depends(get_hall_settings)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/signin',scheme_name="JWT")


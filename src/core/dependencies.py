from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.config.settings import JwtSettings
from fastapi import Depends,Request



def get_jwt_settings(request: Request):
    return request.app.state.settings.jwt


AnnotatedJwtSettings = Annotated[JwtSettings,Depends(get_jwt_settings)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/signin',scheme_name="JWT")
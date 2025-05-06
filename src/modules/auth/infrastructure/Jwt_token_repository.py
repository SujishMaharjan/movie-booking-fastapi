import jwt
from src.modules.auth.interfaces.token_repository import TokenRepository
from datetime import datetime,timedelta,timezone
from src.config.settings import JwtSettings
from src.modules.auth.exceptions import InvalidTokenException



class JwtToken(TokenRepository):

    def __init__(self,jwt_settings: JwtSettings):
        self.jwt_settings = jwt_settings

    def generate_token(self,payload:str)->str:
        to_encode = {"sub":payload}
        expires_delta = timedelta(minutes = self.jwt_settings.access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_settings.secret, algorithm=self.jwt_settings.algorithm)
        return encoded_jwt
    
    def validate_and_decode_token(self,token:str,jwt_settings:JwtSettings)->dict:
        try:
            payload = jwt.decode(token, self.jwt_settings.secret, algorithms=[self.jwt_settings.algorithm])
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Token Expired")
        except jwt.PyJWTError:
            raise InvalidTokenException("Invalid Token")
        return payload

        
        
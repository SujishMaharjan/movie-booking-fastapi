from pydantic import BaseModel  
from src.entrypoints.api.user.models import MemberType  


class UserRegisterResponse(BaseModel):
    name: str
    username: str
    role: MemberType
   
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
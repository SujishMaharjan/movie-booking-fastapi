from pydantic import BaseModel  
from src.api.entrypoint.user.models import MemberType  


class UserRegisterResponse(BaseModel):
    name: str
    username: str
    permission: MemberType
    message: str | None = None
   
    
class Response(BaseModel):
    message: str | None = None
    data: list
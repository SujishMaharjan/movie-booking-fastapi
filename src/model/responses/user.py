from pydantic import BaseModel
from ..user import MemberType 

class UserResponse(BaseModel):
    name : str
    username: str
    permission: MemberType
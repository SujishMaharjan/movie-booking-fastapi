from pydantic import BaseModel

class AllUserResponse(BaseModel):
    username: str
    name: str
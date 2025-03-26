from pydantic import BaseModel
from enum import StrEnum
from typing import Optional


class MemberType(StrEnum):
    admin = "admin"
    member = "member"

class AvailableType(StrEnum):
    available = "Available"
    unavailable = "Unavailable"
    fully_reserved = "Fully Reserved"



class UsersBase(BaseModel):
    name: str
    date_of_birth : str
    email : str
    username : str
    password : str
    permission : MemberType
    user_id : Optional[str] = None

class MovieBase(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str
    movie_id : Optional[str] = None

class ReserveBase(BaseModel):
    username: str
    movie_name: str
    no_of_seats: int
    reserve_id: Optional[str] = None

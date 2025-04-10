from pydantic import BaseModel
from enum import StrEnum
from typing import Optional


class AvailableType(StrEnum):
    available = "Available"
    unavailable = "Unavailable"
    fully_reserved = "Fully Reserved"


class MovieAddModel(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str
    # i think this should be default in db_schemas
    total_seats : Optional[int] = 200
    reserve_seats : Optional[int] = 0
    available_seats : Optional[int] = 200
    # movie_id : Optional[str] = None

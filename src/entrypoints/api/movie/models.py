from pydantic import BaseModel
from enum import StrEnum
from typing import Optional


class StatusType(StrEnum):
    available = "Available"
    fully_reserved = "Fully Reserved"


class MovieAddModel(BaseModel):
    movie_name: str
    movie_description : str
    movie_status : StatusType
    
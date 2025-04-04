from pydantic import BaseModel
from typing import Optional

class ReserveBase(BaseModel):
    movie_name: str
    no_of_seats: int
    reserve_id: Optional[str] = None
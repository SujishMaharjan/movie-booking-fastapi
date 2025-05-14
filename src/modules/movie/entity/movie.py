from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from enum import StrEnum

class StatusType(StrEnum):
    AVAILABLE ="Available" 
    FULLY_RESERVED = "Fully Reserved"

@dataclass
class Movie:
    id: UUID
    movie_name: str
    movie_description: str
    movie_status: StatusType
    total_seats: int
    reserve_seats: int
    available_seats: int
    created_at: datetime

from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Movie:
    id: UUID
    movie_name: str
    movie_description: str
    movie_status: str
    total_seats: int
    reserve_seats: int
    available_seats: int
    created_at: datetime

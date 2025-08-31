from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class Reserve:
    id: uuid
    user_id: uuid
    movie_id: uuid
    user_reserve_seats: int
    created_at: datetime
    updated_at: datetime | None = None
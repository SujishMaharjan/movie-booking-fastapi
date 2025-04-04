from pydantic import BaseModel

class ReserveResponse(BaseModel):
    username: str
    movie_name: str
    user_reserve_seats: int
    # message: Optional[str] = None


class UnReserveResponse(BaseModel):
    username: str
    movie_name: str
    before_reserve_seats: int
    update_reserve_seats: int
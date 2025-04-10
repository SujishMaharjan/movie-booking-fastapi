from pydantic import BaseModel

class ReserveUpdateResponse(BaseModel):
    username: str
    movie_name: str
    user_reserve_seats: int
    before_reserve_seats: int 

class ReserveUserResponse(BaseModel):
    reserve_id: int
    movie_name : str
    user_reserve_seats: str




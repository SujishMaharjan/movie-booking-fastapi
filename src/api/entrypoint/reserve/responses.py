from pydantic import BaseModel

class ReserveResponse(BaseModel):
    reserve_id: int
    username: str
    movie_name: str
    before_reserve_seats: int | None = None
    user_reserve_seats: int
    

class ReserveUserResponse(BaseModel):
    reserve_id: int
    movie_name : str
    user_reserve_seats: str

class ListAllReserveResponse(BaseModel):
    pass




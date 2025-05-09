from pydantic import BaseModel

class ReserveResponse(BaseModel):
    id: str
    username: str
    movie_name: str
    before_reserve_seats: int | None = None
    user_reserve_seats: int
    

class ReserveUserResponse(BaseModel):
    id: str
    user_id : str
    movie_id: str
    user_reserve_seats: int

class UnReserveResponse(ReserveResponse):...

class ListAllReserveResponse(BaseModel):
    pass




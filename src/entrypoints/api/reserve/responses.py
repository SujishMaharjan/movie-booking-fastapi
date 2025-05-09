from pydantic import BaseModel

class ReserveResponse(BaseModel):
    id: str
    username: str
    movie_name: str
    before_reserve_seats: int | None = None
    user_reserve_seats: int
    

class ReserveUserResponse(BaseModel):
    id: str
    movie_name : str
    user_reserve_seats: str

class ListAllReserveResponse(BaseModel):
    pass




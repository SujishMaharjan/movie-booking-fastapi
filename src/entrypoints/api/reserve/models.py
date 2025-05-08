from pydantic import BaseModel

class AddReserveModel(BaseModel):
    movie_id: str
    no_of_seats: int

class UnReserveModel(AddReserveModel): ...


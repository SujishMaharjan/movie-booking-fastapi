from pydantic import BaseModel

class AddReserveModel(BaseModel):
    movie_name: str
    no_of_seats: int

class UnReserveModel(AddReserveModel)
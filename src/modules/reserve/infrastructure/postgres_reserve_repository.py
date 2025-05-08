from sqlalchemy.orm import Session
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.infrastructure.persistence.models import Reservations
from src.modules.reserve.entity.reserve import Reserve
from typing import List,Union
from datetime import datetime


class PostgresReserveRepository(ReserveRepository):
    def __init__(self,session:Session):
        self.session = session

    def save(self,movie:Reservations)->Reservations: ...

    def get_by_id(self, reserve_id: str)-> Union[Reservations,None]: ...

    def get_by_user_id(self, reserve_id: str)-> Union[Reservations,None]: ...

    def get_by_movie_id(self, reserve_id: str)-> Union[Reservations,None]: ...

    def get_all(self)-> Union[List[Reservations],None]: ...

    def get_by_user_id_and_movie_id(self,user_id:str,movie_id:str):
        raw_reserve_obj =self.session.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
        if raw_reserve_obj:
            reserve = self.to_dataclass(raw_reserve_obj,Reserve)
        return reserve

    def to_dataclass(self,object,dataclass_type): ...

    def update_reserve_seats(self,reserve_id,user_reserve_seats,created_at):
        self.session.query(Reservations).filter(Reservations.id == reserve_id).update(
        {Reservations.user_reserve_seats: user_reserve_seats},  # <-- new value
        synchronize_session=False
    )
        return reserve_id


    def to_persistence_model(self,movie:Reserve)->Reservations:...

    def get_by_user_id_and_movie_id(self,user_id:str,movie_id:str):...
        
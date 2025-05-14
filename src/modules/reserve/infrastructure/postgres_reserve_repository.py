from sqlalchemy.orm import Session
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.infrastructure.persistence.models import Reservations
from src.modules.reserve.entity.reserve import Reserve
from typing import List,Union
from datetime import datetime


class PostgresReserveRepository(ReserveRepository):
    def __init__(self,session:Session):
        self.session = session

    def save(self,reserve:Reservations)->Reservations:
        self.session.add(reserve)

    def get_by_id(self, reserve_id: str)-> Union[Reservations,None]:
        raw_reserve =self.session.query(Reservations).filter(Reservations.id == reserve_id).first()
        reserve = self.to_dataclass(raw_reserve,Reserve) if raw_reserve else None
        return reserve

    def get_by_user_id(self, user_id: str)-> Union[Reservations,None]:
        raw_reserve =self.session.query(Reservations).filter(Reservations.user_id == user_id).first()
        reserve = self.to_dataclass(raw_reserve,Reserve) if raw_reserve else None
        return reserve

    def get_by_movie_id(self, reserve_id: str)-> Union[Reservations,None]: ...

    def get_all(self)-> Union[List[Reservations],None]:
        return self.session.query(Reservations).all()

    def get_by_user_id_and_movie_id(self,user_id:str,movie_id:str):
        raw_reserve =self.session.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
        reserve = self.to_dataclass(raw_reserve,Reserve) if raw_reserve else None
        return reserve

    def to_dataclass(self,orm_obj, dataclass_type):
        data = {
            k: v for k, v in vars(orm_obj).items()
            if k in dataclass_type.__dataclass_fields__
        }
        return dataclass_type(**data)

    def update_reserve_seats(self,reserve_id,user_reserve_seats,updated_at):
        updated_rows =self.session.query(Reservations).filter(Reservations.id == reserve_id).update(
            {Reservations.user_reserve_seats : user_reserve_seats,
            Reservations.updated_at : updated_at,
            },  # <-- new value
            synchronize_session=False
        )
        return reserve_id


    def to_persistence_model(self,reserve:Reserve)->Reservations:
        return Reservations(**reserve.__dict__)
    
    def delete_by_id(self,reserve_id:int):
        return self.session.query(Reservations).filter(Reservations.id == reserve_id).delete()
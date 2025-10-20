from sqlalchemy.orm import Session
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.infrastructure.persistence.models import Reservations
from src.modules.reserve.entity.reserve import Reserve
from typing import List,Union
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions import DatabaseException
from src.core.log_config import logger
from src.modules.reserve.exceptions import FailedToPersistException


class PostgresReserveRepository(ReserveRepository):
    def __init__(self,session:Session):
        self.session = session

    def save(self,reserve:Reservations)->Reservations:
        try:
            self.session.add(reserve)
        except SQLAlchemyError as e:
            logger.error("Failed to save user: %s", str(e))
            raise FailedToPersistException(f"An unexpected error occurred while saving user: {str(e)}") from e

    

    def get_by_id(self, reserve_id: str)-> Union[Reservations,None]:
        try: 
            raw_reserve =self.session.query(Reservations).filter(Reservations.id == reserve_id).first()
            reserve = self.to_dataclass(raw_reserve,Reserve) if raw_reserve else None
            return reserve
        except SQLAlchemyError as e:
            logger.error("Database Error during get_by_id : %s",str(e))
            raise DatabaseException("Failed to fetch reservations by id") from e
        

    def get_by_user_id(self, user_id: str)-> Union[Reservations,None]:
        try:
            return self.session.query(Reservations).filter(Reservations.user_id == user_id).all() 
        except SQLAlchemyError as e:
            logger.error("Database Error during get_by_user_id : %s",str(e))
            raise DatabaseException("Failed to fetch reservations by user_id") from e
        


    def get_by_movie_id(self, reserve_id: str)-> Union[Reservations,None]: ...

    def get_all(self)-> Union[List[Reservations],None]:
        try:
            return self.session.query(Reservations).all()
        except SQLAlchemyError as e:
            logger.error("Database Error during get_all")
            raise DatabaseException("Failed to fetch List of reservations") from e
        


    def get_by_user_id_and_movie_id(self,user_id:str,movie_id:str):
        try:
            raw_reserve =self.session.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
            reserve = self.to_dataclass(raw_reserve,Reserve) if raw_reserve else None
            return reserve
        except SQLAlchemyError as e:
            logger.error("Database Error during get by user_id and movie_id")
            raise DatabaseException("Failed to fetch reservations form database") from e
        

    def to_dataclass(self,orm_obj, dataclass_type):
        data = {
            k: v for k, v in vars(orm_obj).items()
            if k in dataclass_type.__dataclass_fields__
        }
        return dataclass_type(**data)

    def update_reserve_seats(self,reserve_id,user_reserve_seats,updated_at):
        try:
            updated_rows =self.session.query(Reservations).filter(Reservations.id == reserve_id).update(
                {Reservations.user_reserve_seats : user_reserve_seats,
                Reservations.updated_at : updated_at,
                },  # <-- new value
                synchronize_session=False
            )
            return reserve_id
        except SQLAlchemyError as e:
            logger.error("Database Error updating reserve seats: %s",str(e))
            raise DatabaseException("Failed to update reservations in database") from e
            


    def to_persistence_model(self,reserve:Reserve)->Reservations:
        return Reservations(**reserve.__dict__)
    
    def delete_by_id(self,reserve_id:int):
        return self.session.query(Reservations).filter(Reservations.id == reserve_id).delete()
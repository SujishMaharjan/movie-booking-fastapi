from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.user.entity.user import User
from src.modules.user.infrastructure.persistence.models import Users
from sqlalchemy.orm import Session
from src.core.exceptions import FailedToPersistException
from src.core.log_config import logger
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions import DatabaseException


class PostgresUserRepository(UserRepository):
    def __init__(self,session: Session):
        self.session = session

    def save(self, user):
        try:
            self.session.add(user)
            self.session.commit()
            logger.debug("User saved successfully in database: %s", user.username)
            
            return True
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to save user: %s %s", str(e),type(e))
            raise FailedToPersistException(f"Failed to save user in database:{type(e)}: {str(e)}") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Failed to save user: %s", str(e))
            raise FailedToPersistException(f"Failed to save user in database: {str(e)}") from e


    def get_by_id(self, user_id):
        try:
            return self.session.query(Users).filter(Users.id == user_id).first()
        except SQLAlchemyError as e:
            logger.error("Database error during get_by_id: %s", str(e))
            raise DatabaseException("Failed to fetch user by ID") from e
        

    def get_by_username(self, username):
        try:
            return  self.session.query(Users).filter(Users.username==username).first()
        except SQLAlchemyError as e:
            logger.error("Database error during get_by_username: %s", str(e))
            raise DatabaseException("Failed to fetch user by username") from e

    
    def get_by_email(self, email):
        try:
            return self.session.query(Users).filter(Users.email==email).first()
        except SQLAlchemyError as e:
            logger.error("Database error during get_by_email: %s", str(e))
            raise DatabaseException("Failed to fetch user by email") from e
        
    
    def get_by_phone(self, phone):
        try:
            return self.session.query(Users).filter(Users.phone==phone).first()
        except SQLAlchemyError as e:
            logger.error("Database error during get_by_phone :%s", str(e))
            raise DatabaseException("Failed to fetch user by phone") from e
        

    
    def get_all(self):
        try:
            return self.session.query(Users).all()
        except SQLAlchemyError as e:
            logger.error("Database error during getting all user : %s", str(e))
            raise DatabaseException("Failed to fetch list of user") from e

    def to_dataclass(self,orm_obj, dataclass_type):
        data = {
            k: v for k, v in vars(orm_obj).items()
            if k in dataclass_type.__dataclass_fields__
        }
        return dataclass_type(**data)
    
    def to_persistence_model(self,user:User)->Users:
        return Users(**user.__dict__)
    

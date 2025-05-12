from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.user.entity.user import User
from src.modules.user.infrastructure.persistence.models import Users
from sqlalchemy.orm import Session
from src.core.exceptions import FailedToPersistException

class PostgresUserRepository(UserRepository):
    def __init__(self,session: Session):
        self.session = session

    def save(self, user):
        try:
            self.session.add(user)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise FailedToPersistException(f"An Unexpected Error Occured while saving user {str(e)}")
        

    def get_by_id(self, user_id):
        return self.session.query(Users).filter(Users.id==user_id).first()
    
    
    def get_by_username(self, username):
        return  self.session.query(Users).filter(Users.username==username).first()

    
    def get_by_email(self, email):
        return self.session.query(Users).filter(Users.email==email).first()
        
    
    def get_by_phone(self, phone):
        return self.session.query(Users).filter(Users.phone==phone).first()
        
    
    def get_all(self):
        return self.session.query(Users).all()

    def to_dataclass(self,orm_obj, dataclass_type):
        data = {
            k: v for k, v in vars(orm_obj).items()
            if k in dataclass_type.__dataclass_fields__
        }
        return dataclass_type(**data)
    
    def to_persistence_model(self,user:User)->Users:
        return Users(**user.__dict__)
    

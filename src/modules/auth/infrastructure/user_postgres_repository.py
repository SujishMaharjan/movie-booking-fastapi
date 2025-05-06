from src.modules.auth.interfaces.user_repository import UserRepository
from src.modules.user.entity.user import User
from src.modules.user.infrastructure.persistence.user import Users
from sqlalchemy.orm import Session


class PostgresUserRepository(UserRepository):
    def __init__(self,session: Session):
        self.session = session

    def save(self, user):
        self.session.add(user)
        self.session.commit()

    def get_by_id(self, user_id):
        user = self.session.query(User).filter(User.id==user_id).first()
        return User(**user)
    
    def get_by_username(self, username):
        user = self.session.query(User).filter(User.username==username).first()
        return User(**user)
    
    def get_by_email(self, email):
        user = self.session.query(User).filter(User.email==email).first()
        return User(**user)
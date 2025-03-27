from models import Users
from sqlalchemy.orm import Session
from schemas import UsersBase

# def create_user(db: Session, data: UsersBase):
#     user_instance = Users(**data.model_dump())
#     db.add(user_instance)
#     db.commit()
#     db.refresh(user_instance)


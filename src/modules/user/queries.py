from src.db_schemas.user import Users
from src.core.extensions import db_dependency
from src.core.extensions import db_dependency as db

# db:db_dependency


def get_user_from_db_by_username(db,username):
    # breakpoint()
    return db.query(Users).filter(Users.username == username).first()


def get_all_users(db):
    return db.query(Users).all()

def get_user_from_db_by_id(db,user_id):
    return db.query(Users).filter(Users.user_id == user_id).first()
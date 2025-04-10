# from src.core.extensions import db_dependency as db
from src.db_schemas.user import Users

# db:db_dependency


def get_user(db,username):
    # breakpoint()
    return db.query(Users).filter(Users.username == username).first()

def save_user_to_db(db,data):
    # breakpoint()
    db.add(data)
    db.commit()
    return get_user(db,data.username)



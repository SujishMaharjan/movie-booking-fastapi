from src.core.infrastucture.persistence.user import Users


# db_session:db_dependency


def get_user_from_db_by_username(db_session,username):
    # breakpoint()
    return db_session.query(Users).filter(Users.username == username).first()


def get_all_users(db_session):
    return db_session.query(Users).all()

def get_user_from_db_by_id(db_session,user_id):
    return db_session.query(Users).filter(Users.user_id == user_id).first()
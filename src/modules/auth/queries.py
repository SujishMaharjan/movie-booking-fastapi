from src.core.infrastucture.persistence.user import Users

def get_user(db_session,username):
    # breakpoint()
    return db_session.query(Users).filter(Users.username == username).first()

def save_user_to_db(db_session,data):
    # breakpoint()
    db_session.add(data)
    db_session.commit()
    return get_user(db_session,data.username)



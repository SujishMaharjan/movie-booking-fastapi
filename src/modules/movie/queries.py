from src.db_schemas.movie import Movies



def get_all_movies_from_db(db_session):
    return db_session.query(Movies).all()

def get_movie_by_movie_name(db_session,movie_name):
    return db_session.query(Movies).filter(Movies.movie_name == movie_name).first()

def get_movie_available_by_movie_name(db_session,movie_name):
    return db_session.query(Movies).filter((Movies.movie_name == movie_name) & (Movies.movie_status == "Available")).first()

def save_movie_to_db(db_session,data):
    db_session.add(data)
    db_session.commit()
    # return True
    return get_movie_by_movie_name(db_session,data.movie_name)

def get_all_movies_available_from_db(db_session):
    movies = db_session.query(Movies).filter(Movies.movie_status == "Available").all()
    return movies

def get_movie_from_db_by_id(db_session,movie_id):
    return db_session.query(Movies).filter(Movies.movie_id == movie_id).first()


def update_movie_after_reserve_or_unreserve_in_db(db_session,movie_id,update_reserve_seats,update_available_seats,movie_status):
        db_session.query(Movies).filter(Movies.movie_id == movie_id).update(
            {Movies.reserve_seats : update_reserve_seats,
            Movies.available_seats : update_available_seats,
            Movies.movie_status : movie_status,
            },  # <-- new value
            synchronize_session=False
        )
        return True
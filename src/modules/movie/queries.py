from src.db_schemas.movie import Movies



def get_all_movies_from_db(db):
    return db.query(Movies).all()

def get_movie_by_movie_name(db,movie_name):
    return db.query(Movies).filter(Movies.movie_name == movie_name).first()

def get_movie_available_by_movie_name(db,movie_name):
    return db.query(Movies).filter((Movies.movie_name == movie_name) & (Movies.movie_status == "Available")).first()

def save_movie_to_db(db,data):
    db.add(data)
    db.commit()
    # return True
    return get_movie_by_movie_name(db,data.movie_name)

def get_all_movies_available_from_db(db):
    movies = db.query(Movies).filter(Movies.movie_status == "Available").all()
    return movies

def get_movie_from_db_by_id(db,movie_id):
    return db.query(Movies).filter(Movies.movie_id == movie_id).first()


def update_movie_after_reserve_or_unreserve_in_db(db,movie_id,update_reserve_seats,update_available_seats,movie_status):
        db.query(Movies).filter(Movies.movie_id == movie_id).update(
            {Movies.reserve_seats : update_reserve_seats,
            Movies.available_seats : update_available_seats,
            Movies.movie_status : movie_status,
            },  # <-- new value
            synchronize_session=False
        )
        return True
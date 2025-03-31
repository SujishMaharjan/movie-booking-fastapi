from models import Movies

def get_movie(db,movie_name):
    movie_names = [movie.movie_name for movie in db.query(Movies).all()]
    if movie_name in movie_names:
        movie = db.query(Movies).filter(Movies.movie_name == movie_name).one()
        return movie
    

    
def check_movie_exist(db,movie_name):
    movie = db.query(Movies).filter(Movies.movie_name == movie_name).first()
    return movie

def add_movie(db,movie):
    movie_dict= movie.model_dump()
    movie_data = Movies(**movie_dict)
    db.add(movie_data)
    db.commit()
    return True
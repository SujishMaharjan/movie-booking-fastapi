from ..database.models import Movies
from ..model.schemas import MovieResponseAvailable
from ..handlers.user_handler import check_user_member_type
from ..model.responses.movie import MovieResponse
from ..exceptions import MemberTypeError,MovieExistError



def get_movie(db,movie_name):
    movie_names = [movie.movie_name for movie in db.query(Movies).all()]
    if movie_name in movie_names:
        movie = db.query(Movies).filter(Movies.movie_name == movie_name).one()
        return movie
    
def get_all_movies_available(db):
    movies = db.query(Movies).filter(Movies.movie_status == "Available").all()
    if not movies:
        return []
    filtered_response_movies = [MovieResponseAvailable(**vars(movie)) for movie in movies]

    return filtered_response_movies

def check_movie_available(db,movie_name):
    movie = db.query(Movies).filter((Movies.movie_name == movie_name)& (Movies.movie_status =="Available")).first()
    return bool(movie)
    
    
def check_movie_exist(db,movie_name):
    movie = db.query(Movies).filter(Movies.movie_name == movie_name).first()
    return bool(movie)

    

def add_movie(db,movie,current_user):
    if not check_user_member_type(current_user,"admin"):
        raise MemberTypeError
    if check_movie_exist(db,movie.movie_name):
        raise MovieExistError
    
    movie_dict= movie.model_dump()
    movie_data = Movies(**movie_dict)
    db.add(movie_data)
    db.commit()

    return MovieResponse(**movie.model_dump())
    
    
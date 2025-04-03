from database.models import Movies
from model.schemas import MovieResponseAvailable
from fastapi.responses import JSONResponse

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

        


def add_movie(db,movie):
    movie_dict= movie.model_dump()
    movie_data = Movies(**movie_dict)
    db.add(movie_data)
    db.commit()
    return True

def update_reserve_seats(self,DATABASE,db_type,no_of_seats=0,no_of_seats_unreserve=0):
        if no_of_seats != 0:
            self._booked_seats += no_of_seats
            self._available_seats -=no_of_seats
            if self._available_seats == 0:
                self._movie_status = "Fully Reserved"
        else:
            self._booked_seats -= no_of_seats_unreserve
            self._available_seats += no_of_seats_unreserve
            if self._available_seats != 0:
                self._movie_status = "Available"

        self.add_movie(DATABASE,db_type)
        return True
        
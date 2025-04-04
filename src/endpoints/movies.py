from fastapi import APIRouter,Depends
from typing import Annotated
from ..log import logger
from ..handlers.movie_handler import add_movie,get_all_movies_available
from ..dependencies import db_dependency
from ..exceptions import FailedToAddMovieError
from ..model.movie import MovieBase
from ..auth.auth import get_current_user
from ..database.models import Users

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


@router.post("")
async def add_movies(db:db_dependency,movie :MovieBase, current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("movies endpoint accessed")
    movie_response = add_movie(db,movie,current_user)
    if not movie_response:
        raise FailedToAddMovieError
    
    return movie_response

    # #checks current_user has permission role "admin" as only admin can add movies
    # if not user_handler.check_user_member_type(current_user,"admin"):
    #     return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    # if movie_handler.check_movie_exist(db,movie.movie_name):
    #     return JSONResponse(status_code=409, content={'detail':'Movie already exist'})
    # if not movie_handler.add_movie(db,movie):
    #     return JSONResponse(content={'detail':"Error in adding movies"})
    # logger.info(f"{movie.movie_name} added by {current_user.username}")
    # return MovieResponse(**movie.model_dump())

    
 
@router.get("")
async def show_available_movies(db:db_dependency):
    logger.info("movies endpoint accessed")
    movies = get_all_movies_available(db)
    return movies

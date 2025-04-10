from fastapi import APIRouter,Request,Depends
from src.api.entrypoint.movie import models,responses
from src.db_schemas.user import Users
from src.modules.movie.handlers import (
    get_movies,
    check_duplicate_movie,
    persist_movie_to_db,
    get_all_movies_available  
)
from src.modules.user.handlers import check_user_member_type
from src.core.extensions import db_dependency
from typing import Annotated
from src.modules.auth.handlers import get_current_user



router = APIRouter(prefix="/movies",tags=["Movie"])


@router.get("/")
async def list_movies_resource(request: Request):
    movies = get_movies()
    return movies
    

@router.post("/",status_code=401)
async def add_movies_resource(
    request: Request,
    model: models.MovieAddModel ,
    db:db_dependency,
    current_user:Annotated[Users, Depends(get_current_user)]
    ):

    check_user_member_type(current_user,"admin")
    check_duplicate_movie(model.movie_name)
    persist_movie_to_db(model)

    return responses.MovieAddResponse(model)

@router.post("/Available/")
async def show_available_movies():
    movies = get_all_movies_available()
    return movies



    


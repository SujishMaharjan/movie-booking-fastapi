from fastapi import APIRouter,Request,Depends
from src.api.entrypoint.movie import models,responses
from src.db_schemas.user import Users
from src.modules.movie.handlers import (
    get_all_movies,
    check_duplicate_movie,
    persist_movie_to_db,
    get_all_movies_available ,
    get_movie_by_id
)
from src.modules.user.handlers import check_user_member_type
from src.core.extensions import db_dependency
from typing import Annotated
from src.modules.auth.handlers import get_current_user



router = APIRouter(prefix="/movies",tags=["Movie"])


@router.get("/")
async def list_movies_resource(request: Request,db:db_dependency):
    movies = get_all_movies(db)
    return movies
    

@router.post("/")
async def add_movies_resource(
    request: Request,
    model: models.MovieAddModel ,
    db:db_dependency,
    current_user:Annotated[Users, Depends(get_current_user)]
    ):
    check_user_member_type(current_user,"admin")
    check_duplicate_movie(db,model.movie_name)
    movie = persist_movie_to_db(db,model)

    return movie

@router.get("/available/")
async def show_available_movies(request: Request,db:db_dependency):
    movies = get_all_movies_available(db)
    return movies


@router.get("/{movie_id}")
async def get_movie_resource(request: Request,db:db_dependency,movie_id:int,current_user:Annotated[Users, Depends(get_current_user)]): 
    check_user_member_type(current_user,"admin")
    movie = get_movie_by_id(db,movie_id)
    return movie


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...


    


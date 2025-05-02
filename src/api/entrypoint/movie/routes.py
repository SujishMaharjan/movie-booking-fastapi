from fastapi import APIRouter, Request, Depends,Form
from src.api.entrypoint.movie import models, responses
from src.db_schemas.user import Users
from src.modules.movie.handlers import (
    get_all_movies,
    check_duplicate_movie,
    persist_movie_to_db,
    get_all_movies_available,
    get_movie_by_id,
)
from src.modules.user.handlers import check_user_member_type
from src.core.extensions import get_db_session
from sqlalchemy.orm import Session
from typing import Annotated
from src.modules.auth.handlers import get_current_user


router = APIRouter(prefix="/movies", tags=["Movie"])


@router.get("/")
async def list_movies_resource(
    request: Request, db_session: Session = Depends(get_db_session)
):

    movies = get_all_movies(db_session)
    return movies


@router.post("/")
async def add_movies_resource(
    request: Request,
    model: models.MovieAddModel,
    current_user: Users = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    check_user_member_type(current_user, "admin")
    check_duplicate_movie(db_session, model.movie_name)
    movie = persist_movie_to_db(db_session, model)

    return movie


@router.get("/available/")
async def show_available_movies(
    request: Request,
    db_session: Session=Depends(get_db_session)
):
    movies = get_all_movies_available(db_session)
    return movies


@router.get("/{movie_id}")
async def get_movie_resource(
    request: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
    movie_id: int,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    check_user_member_type(current_user, "admin")
    movie = get_movie_by_id(db_session, movie_id)
    return movie


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...

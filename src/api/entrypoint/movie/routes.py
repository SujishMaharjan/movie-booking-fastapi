from fastapi import APIRouter, Request, Depends
from src.api.entrypoint.movie import models, responses
from src.core.infrastucture.persistence.database_postgres import get_db_session
from sqlalchemy.orm import Session
from typing import Annotated
from src.core.dependencies import oauth2_scheme,AnnotatedJwtSettings,AnnotatedHallSettings
from src.modules.auth.infrastructure.Jwt_token_repository import JwtToken
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.movie.application.add_movies import CreateMovie


router = APIRouter(prefix="/movies", tags=["Movie"])


# @router.get("/")
# async def list_movies_resource(
#     request: Request, db_session: Session = Depends(get_db_session)
# ):

#     movies = get_all_movies(db_session)
#     return movies


@router.post("/")
async def add_movies_resource(
    request: Request,
    movie_model: models.MovieAddModel,
    hall_settings: AnnotatedHallSettings,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    token_repo = JwtToken(jwt_settings)
    user_repo = PostgresUserRepository(db_session)
    movie_repo = PostgresMovieRepository(db_session)
    new_movie = CreateMovie(user_repo,token_repo,movie_repo).execute(token,movie_model,hall_settings)
    return responses.MovieAddResponse(**new_movie)


# @router.get("/available/")
# async def show_available_movies(
#     request: Request,
#     db_session: Session=Depends(get_db_session)
# ):
#     movies = get_all_movies_available(db_session)
#     return movies


# @router.get("/{movie_id}")
# async def get_movie_resource(
#     request: Request,
#     db_session: Annotated[Session, Depends(get_db_session)],
#     movie_id: int,
#     current_user: Annotated[Users, Depends(get_current_user)],
# ):
#     check_user_member_type(current_user, "admin")
#     movie = get_movie_by_id(db_session, movie_id)
#     return movie


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...

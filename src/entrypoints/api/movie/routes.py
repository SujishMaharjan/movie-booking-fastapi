from fastapi import APIRouter, Request, Depends
from src.entrypoints.api.movie import models, responses
from src.core.infrastucture.persistence.database_postgres import get_db_session
from sqlalchemy.orm import Session
from typing import Annotated
from src.core.dependencies import oauth2_scheme,AnnotatedJwtSettings,AnnotatedHallSettings
from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.movie.application.add_movies import CreateMovie
from src.modules.movie.application.list_available_movies import GetAvailableMovies
from src.entrypoints.api.movie.responses import MovieResponseAvailable, AllMovieResponse,MovieIdResponse
from src.modules.movie.application.list_movies import GetMovies
from src.modules.movie.application.get_movie_by_id import GetMovieById


router = APIRouter(prefix="/movies", tags=["Movie"])


@router.get("/")
async def list_movies_resource(
    request: Request,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    token_repo = JwtService(jwt_settings)
    user_repo = PostgresUserRepository(db_session)
    movie_repo=PostgresMovieRepository(db_session)
    movies = GetMovies(token,user_repo,token_repo,movie_repo).execute()
    return [AllMovieResponse(**movie.__dict__) for movie in movies]



@router.post("/")
async def add_movies_resource(
    request: Request,
    movie_model: models.MovieAddModel,
    hall_settings: AnnotatedHallSettings,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    token_repo = JwtService(jwt_settings)
    user_repo = PostgresUserRepository(db_session)
    movie_repo = PostgresMovieRepository(db_session)
    new_movie = CreateMovie(user_repo,token_repo,movie_repo).execute(token,movie_model,hall_settings)
    return responses.MovieAddResponse(**new_movie.__dict__)


@router.get("/available/")
async def show_available_movies(
    request: Request,
    db_session: Session=Depends(get_db_session)
):
    movie_repo = PostgresMovieRepository(db_session)
    movies = GetAvailableMovies(movie_repo).exeute()
    return [MovieResponseAvailable(**movie.__dict__) for movie in movies]

@router.get("/{movie_id}")
async def get_movie_resource(
    request: Request,
    movie_id:str,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    token_repo = JwtService(jwt_settings)
    user_repo = PostgresUserRepository(db_session)
    movie_repo=PostgresMovieRepository(db_session)
    movie = GetMovieById(token,user_repo,token_repo,movie_repo).execute(movie_id)
    
    return MovieIdResponse(**movie.__dict__)


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...

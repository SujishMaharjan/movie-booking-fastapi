from fastapi import APIRouter, Request, Depends
from src.entrypoints.api.movie import models, responses
from src.core.database import get_db_session

from src.core.dependencies import(
    AnnotatedHallSettings,
    AnnotatedRepositoryProvider,
    AnnotatedCurrentUser
)
from src.modules.movie.application.add_movies import CreateMovie
from src.modules.movie.application.list_available_movies import GetAvailableMovies
from src.entrypoints.api.movie.responses import MovieResponseAvailable, AllMovieResponse,MovieIdResponse
from src.modules.movie.application.list_movies import GetMovies
from src.modules.movie.application.get_movie_by_id import GetMovieById
from src.core.security import is_admin,is_member
from src.core.log_config import logger


router = APIRouter(prefix="/movies", tags=["Movie"])


@router.get("/")
async def list_movies_resource(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    logger.info("User %s trying to access movies list",user.username)
    is_admin(user)
    movies = GetMovies(provider).execute()
    logger.debug("Retrieved %d movies", len(movies))
    return [AllMovieResponse(**vars(movie)) for movie in movies if movies]



@router.post("/")
async def add_movies_resource(
    request: Request,
    movie_model: models.MovieAddModel,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser,
    hall_settings: AnnotatedHallSettings
):
    logger.info("Movie add request received for movie: %s", movie_model.movie_name)
    is_admin(user)
    new_movie = CreateMovie(provider).execute(movie_model,hall_settings)
    return responses.MovieAddResponse(**vars(new_movie))


@router.get("/available/")
async def show_available_movies(
    request: Request,
    provider:AnnotatedRepositoryProvider
):
    logger.info("Request recieved for available movies")
    movies = GetAvailableMovies(provider).exeute()
    logger.debug("Retrieved %d movies", len(movies))
    return [MovieResponseAvailable(**vars(movie)) for movie in movies]

@router.get("/{movie_id}")
async def get_movie_resource(
    request: Request,
    movie_id:str,
    provider:AnnotatedRepositoryProvider,
    user:AnnotatedCurrentUser
):
    logger.info("User %s requested info for movie details %s", user.id, movie_id)
    is_admin(user)
    movie = GetMovieById(provider).execute(movie_id)
    logger.debug("Retrieved data for movie %s", movie_id)
    return MovieIdResponse(**vars(movie))


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...

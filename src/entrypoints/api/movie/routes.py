from fastapi import APIRouter, Request
from src.entrypoints.api.movie import models, responses
from src.core.dependencies import AnnotatedCurrentUser,AnnotatedHallSettings,AnnotatedRepositoryProvider
from src.modules.movie.application import movie_service
from src.entrypoints.api.movie.responses import MovieResponseAvailable, AllMovieResponse,MovieIdResponse
from src.core.security import is_admin
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
    movies = movie_service.list_movies(provider)
    logger.debug("Retrieved %d movies", len(movies))
    return [AllMovieResponse(**vars(movie)) for movie in movies if movies]



@router.post("/")
async def add_movies_resource(
    request: Request,
    movie_model: models.MovieAddModel,
    hall_settings: AnnotatedHallSettings,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser,
):
    logger.info("Movie add request received for movie: %s", movie_model.movie_name)
    is_admin(user)
    new_movie = movie_service.create_movie_service(movie_model,hall_settings,provider)
    return responses.MovieAddResponse(**vars(new_movie))


@router.get("/available/")
async def show_available_movies(
    request: Request,
    provider: AnnotatedRepositoryProvider,
):
    logger.info("Request recieved for available movies")
    movies = movie_service.get_available_movies(provider)
    logger.debug("Retrieved %d movies", len(movies))
    return [MovieResponseAvailable(**vars(movie)) for movie in movies]

@router.get("/{movie_id}")
async def get_movie_resource(
    request: Request,
    movie_id:str,
    provider: AnnotatedRepositoryProvider,
    user:AnnotatedCurrentUser
):
    logger.info("User %s requested info for movie details %s", user.id, movie_id)
    is_admin(user)
    movie = movie_service.get_movie_by_id(movie_id,provider)
    logger.debug("Retrieved data for movie %s", movie_id)
    return MovieIdResponse(**vars(movie))


# @router.patch("/{movie_id}")
# async def update_movie_resource(request: Request): ...

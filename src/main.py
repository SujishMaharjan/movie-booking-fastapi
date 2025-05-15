from fastapi import FastAPI
from src.entrypoints.api.auth.routes import router as auth_router
from src.entrypoints.api.user.routes import router as user_router
from src.entrypoints.api.movie.routes import router as movie_router
from src.entrypoints.api.reserve.routes import router as reserve_router
from src.core.lifespan import lifespan
from src.entrypoints.middlewares import CustomExceptionMiddleware
from src.core.log_config import logger
# from src.modules.user.interfaces.user_repository import UserRepository
# from src.modules.auth.interfaces.token_repository import TokenRepository
# from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
# from src.modules.movie.interfaces.movie_repository import MovieRepository
# from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
# from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
# from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
# from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher
# from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
# from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from src.core.provider import Provider
from src.core.dependencies import get_provider




def init_app():
    app = FastAPI(lifespan=lifespan)

    #adding routes
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(movie_router)
    app.include_router(reserve_router)
    logger.info("All Routers Registered")

    #adding middlewares
    app.add_middleware(CustomExceptionMiddleware)
    logger.info("Custom exception middleware added")

    #overiding repositories
    logger.info("Adding Repositoriers")
    # app.dependency_overrides[UserRepository] = PostgresUserRepository
    # app.dependency_overrides[TokenRepository] = JwtService
    # app.dependency_overrides[PasswordHasher] = BcryptPasswordHasher
    # app.dependency_overrides[MovieRepository] = PostgresMovieRepository
    # app.dependency_overrides[ReserveRepository] = PostgresReserveRepository
    # app.dependency_overrides[Provider] = get_provider

    logger.info("Application initialization complete")
    return app

app = init_app()
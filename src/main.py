from fastapi import FastAPI
from src.entrypoints.api.auth.routes import router as auth_router
from src.entrypoints.api.user.routes import router as user_router
from src.entrypoints.api.movie.routes import router as movie_router
from src.entrypoints.api.reserve.routes import router as reserve_router
from src.core.lifespan import lifespan
from src.entrypoints.middlewares import CustomExceptionMiddleware
from src.core.log_config import logger



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

    logger.info("Application initialization complete")
    return app

app = init_app()
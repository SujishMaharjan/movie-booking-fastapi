from fastapi import FastAPI
from src.api.entrypoint.auth.routes import router as auth_router
from src.api.entrypoint.user.routes import router as user_router
from src.api.entrypoint.movie.routes import router as movie_router
# from src.api.entrypoint.reserve.routes import router as reserve_router
from src.core.lifespan import lifespan
from src.api.middlewares import CustomExceptionMiddleware



def init_app():
    app = FastAPI(lifespan=lifespan)

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(movie_router)
    # app.include_router(reserve_router)

    app.add_middleware(CustomExceptionMiddleware)

    return app

app = init_app()
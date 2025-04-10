from fastapi import FastAPI
from src.api.entrypoint.auth.routes import router as auth_router
from src.core.lifespan import lifespan
from src.core.middlewares import CustomExceptionMiddleware

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

app.add_middleware(CustomExceptionMiddleware)

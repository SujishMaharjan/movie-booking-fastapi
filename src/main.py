from fastapi import FastAPI,Response
from .database.database import engine,Base
from contextlib import asynccontextmanager
from .log import logger
from .endpoints.users import router as users_router
from .endpoints.movies import router as movies_router
from .endpoints.reserves import router as reserves_router



@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Application startup: Logger initialized")
    yield
    logger.info("Application shutdown: Logger closing")

app = FastAPI(lifespan=lifespan)
Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(movies_router)
app.include_router(reserves_router)



@app.get("/")
async def read_root():
    return Response("Server is Running")





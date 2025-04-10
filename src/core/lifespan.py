from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.log_config import logger
from src.core.extensions import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: Logger initialized")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Application shutdown: Logger closing")

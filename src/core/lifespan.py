import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.log_config import logger
from src.config.settings import AppSettings,JwtSettings
from src.core.database import create_db_engine,init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Application startup: Logger initialized")
    app.state.settings = AppSettings()
    logger.info("Configuration Loaded")
    app.state.engine = await asyncio.to_thread(create_db_engine,app.state.settings.database)
    logger.debug("Database Engine Created")
    await asyncio.to_thread(init_db, app.state.engine)
    
    yield
    logger.info("Application shutdown: Logger closing")

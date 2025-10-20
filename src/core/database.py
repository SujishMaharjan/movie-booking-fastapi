from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends,Request
from src.config.settings import DatabaseSettings
from src.core.log_config import logger
from sqlalchemy import inspect

Base = declarative_base()

def create_db_engine(database: DatabaseSettings):
    engine = create_engine(
        f"postgresql://{database.user}:{database.password}@{database.host}:{database.port}/{database.name}"
    )
    return engine

def init_db(engine):
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    if existing_tables:
        logger.debug("Database already initialized. Tables found: %s", existing_tables)
    else:
        logger.debug("No tables found. Creating database schema...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")


def get_db_session(request: Request):
    engine = request.app.state.engine
    with Session(engine) as session:
        yield session

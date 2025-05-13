import click
from src.config.settings import AppSettings
from sqlalchemy import create_engine
from src.core.infrastucture.persistence.database_postgres import Base,create_db_engine




def init_database_tables_via_cli():
    engine= create_db_engine(AppSettings().database)
    Base.metadata.create_all(bind=engine)


    

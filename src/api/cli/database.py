from src.config.settings import AppSettings
from sqlalchemy import create_engine
from src.core.infrastucture.persistence.database_postgres import Base,init_db




def init_database_via_cli():
    database = AppSettings().database
    engine = create_engine(
        f"postgresql://{database.user}:{database.password}@{database.host}:{database.port}/{database.name}"
    )
    Base.metadata.create_all(bind=engine)

init_database_via_cli()
    

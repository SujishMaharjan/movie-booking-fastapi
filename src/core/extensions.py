
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends,Request
from src.config.settings import DatabaseSettings

_engine = None
# #postgres url
# URL_DATABASE = 'postgresql://postgres:password@localhost:5432/movie_db'

# #creating engine 
# engine = create_engine(URL_DATABASE)

# SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()


def create_db_engine(database: DatabaseSettings):
    engine = create_engine(
        f"postgresql://{database.user}:{database.password}@{database.host}:{database.port}/{database.name}"
    )
    return engine

def init_db(engine):
    Base.metadata.create_all(bind=engine)


def get_db_session(request: Request):
    engine = request.app.state.engine
    with Session(engine) as session:
        yield session

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def create_table():
#     Base.metadata.create_all(bind=engine)
    
# #database dependency
# db_dependency = Annotated[Session, Depends(get_db)]
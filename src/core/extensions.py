
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends
from typing import Annotated


#postgres url
URL_DATABASE = 'postgresql://postgres:password@localhost:5432/movie_db'

#creating engine 
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)
    
#database dependency
db_dependency = Annotated[Session, Depends(get_db)]
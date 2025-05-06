from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel,SecretStr,Field
from fastapi import Request
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import uuid
# class DatabaseSettings(BaseModel):
#     user: str
#     password: str
#     host: str
#     port: int
#     name: str



# class AppSettings(BaseSettings):
#     database: DatabaseSettings# = Field(validation_alias='database')

    
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding='utf-8'
#         )

    



Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(String,primary_key=True,index=True)
    name = Column(String, index=True,nullable=False)
    phone = Column(String, index=True,nullable=False)
    email = Column(String, index=True,nullable=False)
    username = Column(String, index=True)
    hashed_password = Column(String)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))
    role = Column(String)
    
    
    

class Reservations(Base):
    __tablename__ = "reservations"

    reserve_id = Column(Integer,primary_key=True,index=True)
    user_reserve_seats = Column(Integer)

class Reservations_two(Base):
    __tablename__ = "reservations_two"

    reserve_id = Column(Integer,primary_key=True,index=True)
    user_reserve_seats = Column(Integer)

database={
  "user": "postgres",
  "password": "password",
  "host": "localhost",
  "port": 5432,
  "name": "movie_db"
}   

def create_db_engine():
    engine = create_engine(
        f"postgresql://{database["user"]}:{database["password"]}@{database["host"]}:{database["port"]}/{database["name"]}"
    )
    return engine

engine = create_db_engine()

def init_db(engine):
    breakpoint()
    Base.metadata.create_all(bind=engine)

init_db(engine)



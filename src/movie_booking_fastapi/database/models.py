from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Relationship


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True,nullable=False)
    date_of_birth =Column(DateTime)
    email = Column(String)
    username = Column(String, index=True)
    password = Column(String)
    permission = Column(String)
    disabled = Column(Boolean, default=False)
    # created_at =Column(DateTime, default=datetime.now(timezone.utc))
    
    

class Movies(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer,primary_key=True,index=True)
    movie_name = Column(String, index=True)
    movie_description =Column(String)
    movie_status = Column(String)
    total_seats = Column(Integer, index=True)
    reserve_seats = Column(Integer,index=True)
    available_seats = Column(Integer,index=True)

    



class Reservations(Base):
    __tablename__ = "reservations"

    reserve_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.user_id"),index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"),index=True)
    user_reserve_seats = Column(Integer)

   
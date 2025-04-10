from src.core.extensions import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone

class Reservations(Base):
    __tablename__ = "reservations"

    reserve_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.user_id"),index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"),index=True)
    user_reserve_seats = Column(Integer)

   
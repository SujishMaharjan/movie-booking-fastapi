from src.core.infrastucture.persistence.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone

class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(String,primary_key=True,index=True)
    user_id = Column(String,ForeignKey("users.id"),index=True)
    movie_id = Column(String, ForeignKey("movies.id"),index=True)
    user_reserve_seats = Column(Integer)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))
    updated_at =Column(DateTime,nullable=True) 


   
from src.core.infrastucture.persistence.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer,primary_key=True,index=True)
    movie_name = Column(String, index=True)
    movie_description =Column(String)
    movie_status = Column(String)
    total_seats = Column(Integer, index=True)
    reserve_seats = Column(Integer,index=True)
    available_seats = Column(Integer,index=True)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))

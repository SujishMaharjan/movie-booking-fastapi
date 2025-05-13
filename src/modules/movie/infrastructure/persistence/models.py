from src.core.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime,Enum
from datetime import datetime, timezone
from src.modules.movie.entity.movie import StatusType

class Movies(Base):
    __tablename__ = "movies"

    id = Column(String,primary_key=True,index=True)
    movie_name = Column(String, index=True)
    movie_description =Column(String)
    movie_status = Column(Enum(StatusType))
    total_seats = Column(Integer, index=True)
    reserve_seats = Column(Integer,index=True)
    available_seats = Column(Integer,index=True)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))

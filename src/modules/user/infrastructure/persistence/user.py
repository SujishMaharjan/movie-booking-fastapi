from src.core.infrastucture.persistence.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone

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
    
    
    


    

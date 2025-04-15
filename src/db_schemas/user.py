from src.core.extensions import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone



class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True,nullable=False)
    date_of_birth =Column(DateTime)
    email = Column(String)
    username = Column(String, index=True)
    password = Column(String)
    permission = Column(String)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))
    
    


    

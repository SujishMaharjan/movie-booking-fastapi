from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel,SecretStr,Field
from fastapi import Request
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import uuid
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime | None = None


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(String,primary_key=True,index=True)
    created_at =Column(DateTime, default=datetime.now(timezone.utc))
    updated_at =Column(DateTime,nullable=True, default=datetime.now(timezone.utc))
    
    
    
    
user = User(
    id="id1",
    created_at=datetime.now()
)

orm_user = Users(**user.__dict__)

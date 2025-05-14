from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel,SecretStr,Field
from fastapi import Request
from pathlib import Path

class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

class TokenSettings(BaseModel):...

class JwtSettings(TokenSettings):
    secret: str
    algorithm: str
    access_token_expire_minutes: int

class HallSettings(BaseModel):
    seat_capacity: int


# env_path = Path(__file__).resolve().parent.parent / ".env"

class AppSettings(BaseSettings):
    database: DatabaseSettings# = Field(validation_alias='database')
    jwt: JwtSettings# = Field(alias='default2') 
    hall: HallSettings
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
        )

   
    
def get_default_settings(request: Request):
    return request.app.state.settings.default

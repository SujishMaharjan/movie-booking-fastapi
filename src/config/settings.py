from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel,SecretStr,Field
from fastapi import Request

class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

class DefaultSettings(BaseModel):
    secret: str
    algorithm: str
    access_token_expire_minutes: int


class AppSettings(BaseSettings):
    database: DatabaseSettings# = Field(validation_alias='database')

    default: DefaultSettings# = Field(alias='default2') 
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
        )

   
    
def get_default_settings(request: Request):
    return request.app.state.settings.default

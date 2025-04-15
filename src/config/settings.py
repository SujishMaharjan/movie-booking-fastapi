from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel,field_validator,SecretStr
import json

class DefaultSettings(BaseModel):
    secret: str
    algorithm: str
    access_token_expire_minutes: int


class AppSettings(BaseSettings):
    default: DefaultSettings

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("default", mode="before")
    @classmethod
    def parse_default(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
from abc import ABC,abstractmethod
from datetime import timedelta
from src.config.settings import TokenSettings

class TokenRepository(ABC):
   
    def generate_token(self, payload:str,token_settings: TokenSettings)-> str: ...

    def validate_and_decode_token(self, token:str)-> dict: ...

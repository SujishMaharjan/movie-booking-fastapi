import jwt
from src.modules.auth.application.ports.token_repository import TokenRepository
from datetime import datetime,timedelta,timezone
from src.config.settings import JwtSettings
from src.modules.auth.exceptions import InvalidTokenException
from src.core.log_config import logger



class JwtService(TokenRepository):
    """
    Service class to handle JWT token generation and validation.
    """

    def __init__(self,jwt_settings: JwtSettings):
        """
        Initializes the JWT service with the given settings.

        Args:
            jwt_settings (JwtSettings): Configuration for JWT such as secret key, algorithm, and expiration.
        """
        self.jwt_settings = jwt_settings

    def generate_token(self,payload:str)->str:
        """
        Generates a JWT token for the given user payload which has username.

        Args:
            payload (str): A unique identifier for the user (usually user ID or username).

        Returns:
            str: Encoded JWT token.
        """
        logger.debug("Generating token for user :%s",payload)
        try:
            to_encode = {"sub":payload}
            expires_delta = timedelta(minutes = self.jwt_settings.access_token_expire_minutes)
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.jwt_settings.secret, algorithm=self.jwt_settings.algorithm)
            logger.debug("Token Generation Successfull for user: %s", payload)
            return encoded_jwt
        except Exception as e:
            logger.error("Unexpected error occured during token generations: %s",str(e))
            raise RuntimeError("Internal error during token generation") from e
    
    def validate_and_decode_token(self,token:str)->dict:
        """
        Validates and decodes a JWT token.

        Args:
            token (str): The JWT token to validate and decode.

        Returns:
            str: The 'sub' (subject) claim from the token if valid (has a username).

        Raises:
            InvalidTokenException: If the token is expired or invalid.
        """
        try:
            logger.debug("Validating and decoding token")
            payload = jwt.decode(token, self.jwt_settings.secret, algorithms=[self.jwt_settings.algorithm])
            logger.debug("Validation and decoding of token Successful")
            # username = payload.get("sub")
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("user attempt to use and expired token")
            raise InvalidTokenException("Token Expired")
        except jwt.PyJWTError:
            logger.warning("user attempt to use an invalid token")
            raise InvalidTokenException("Invalid Token")
        

    
        
        
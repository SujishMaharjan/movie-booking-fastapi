from src.modules.user.entity.user import User
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.auth.exceptions import LoginException
from src.core.provider import Provider
from src.core.log_config import logger



class LoginUser:
    def __init__(self,provider:Provider):
        self.user_repository:UserRepository = provider.user_repository
        self.hasher_repository:PasswordHasher = provider.password_hasher_repository
        self.token_repository:TokenRepository = provider.token_repository
        

    def execute(self,identifier,password):
        logger.debug("Login attempt started for identifier: %s", identifier)
        try:
            # Logic to handle login using identifier (username, email, or phone) and password
            user = self.user_repository.get_by_username(identifier)
            if not user:
                user = self.user_repository.get_by_phone(identifier)
            if not user:
                user = self.user_repository.get_by_email(identifier)
            if not user:
                logger.warning("Invalid Login attempt with identifier: %s", identifier)
                raise LoginException("Invalid Username Or Password")
            
            logger.info("User found with identifier: %s", identifier)
            user = self.user_repository.to_dataclass(user,User)

            self.hasher_repository.verify_password(password=password,hashed=user.hashed_password)
            logger.info("Password verified for user: %s", user.username)
            token=self.token_repository.generate_token(payload=user.username)
            logger.debug("Token generated for user: %s", user.username)
            return token
        except Exception as e:
            logger.error("Error occured while logging in by user :%s",identifier)
            raise


        



    
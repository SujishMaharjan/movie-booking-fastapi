from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.core.provider import Provider
from src.core.log_config import logger


class GetUser:
    """
    Application service for retrieving a user by ID.
    """
    def __init__(self,provider:Provider):
        """
        Args:
            provider (Provider): Provides access to repositories (e.g., UserRepository).
        """
        self.user_repo:UserRepository = provider.user_repository
    
    def execute(self,user_id:int):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user data as a domain/dataclass object.

        Raises:
            UserNotFoundException: If no user with the given ID exists.
        """
        try:
            raw_user = self.user_repo.get_by_id(user_id)
            if not raw_user:
                logger.warning("User not found with ID: %s", user_id)
                raise UserNotFoundException(f"No user with such id {user_id}")
            user = self.user_repo.to_dataclass(raw_user,User)
            logger.debug("User found and converted for ID: %s", user_id)
            return user
        except Exception as e:
            logger.error("Error fetching user profile for %s:", user_id)
            raise 
    
    

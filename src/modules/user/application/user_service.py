from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.user.exceptions import UserNotFoundException
from src.modules.user.entity.user import User
from src.core.provider import Provider
from src.core.log_config import logger



def get_user_by_id(user_id:int,provider:Provider):
    user_repo:UserRepository = provider.user_repository
    try:
        raw_user = user_repo.get_by_id(user_id)
        if not raw_user:
            logger.warning("User not found with ID: %s", user_id)
            raise UserNotFoundException(f"No user with such id {user_id}")
        user = user_repo.to_dataclass(raw_user,User)
        logger.debug("User found and converted for ID: %s", user_id)
        return user
    except Exception as e:
        logger.error("Error fetching user profile for %s:", user_id)
        raise 
    
    
def list_users(provider: Provider):
        user_repo:UserRepository = provider.user_repository
        logger.debug("List Attempt Started")
        try:
            users = user_repo.get_all()
            users = [user_repo.to_dataclass(user,User) for user in users] if users else []
            return users
        except Exception as e:
            logger.exception("An unexpected error occured while listing user")
            raise
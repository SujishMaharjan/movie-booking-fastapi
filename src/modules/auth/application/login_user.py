from src.modules.user.entity.user import User,UserRole
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.application.ports.password_hasher_repository import PasswordHasher
from src.modules.auth.application.ports.token_repository import TokenRepository
from src.modules.auth.exceptions import LoginException,InvalidMemberTypeException
from src.core.provider import Provider
from src.core.log_config import logger



def login_user_service(identifier,password,provider:Provider):
    logger.debug("Login attempt started for identifier: %s", identifier)
    user_repo:UserRepository = provider.user_repository
    hasher_repo:PasswordHasher = provider.password_hasher_repository
    token_repo:TokenRepository = provider.token_repository
    
    try:
        # Logic to handle login using identifier (username, email, or phone) and password
        user = user_repo.get_by_username(identifier)
        if not user:
            user = user_repo.get_by_phone(identifier)
        if not user:
            user = user_repo.get_by_email(identifier)
        if not user:
            logger.warning("Invalid Login attempt with identifier: %s", identifier)
            raise LoginException("Invalid Username Or Password")
        
        logger.info("User found with identifier: %s", identifier)
        user = user_repo.to_dataclass(user,User)

        hasher_repo.verify_password(password=password,hashed=user.hashed_password)
        logger.info("Password verified for user: %s", user.username)
        token=token_repo.generate_token(payload=user.username)
        logger.debug("Token generated for user: %s", user.username)
        return token
    except Exception as e:
        logger.error("Error occured while logging in by user :%s",identifier)
        raise






# def is_admin(user:User):
#     logger.debug("Checking whether user is admin")
#     if user.role!=UserRole.ADMIN:
#         logger.warning("Unauthorize user: %s trying to access",user.username)
#         raise InvalidMemberTypeException("Access denied. Admin only.")
#     return True

# def is_member(user:User):
#     logger.debug("Checking whether user is member")
#     if user.role!=UserRole.MEMBER:
#         logger.warning("Unauthorize user: %s trying to access",user.username)
#         raise InvalidMemberTypeException("Access denied. Member only.")
#     return True


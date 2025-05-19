import uuid
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.application.ports.password_hasher_repository import PasswordHasher
from src.modules.auth.application.ports.token_repository import TokenRepository
from src.modules.user.entity.user import User, UserRole
from datetime import datetime
from src.modules.user.infrastructure.persistence.models import Users
from src.modules.auth.exceptions import DuplicateUserException
from src.core.provider import Provider
from src.modules.auth.application.ports.password_hasher_repository import PasswordHasher
from src.core.log_config import logger


 

def register_user_service(name, username, password, phone, email,provider:Provider):
    logger.info("Registering user with username : %s" ,username)
    user_repo:UserRepository = provider.user_repository
    hasher_repo:PasswordHasher = provider.password_hasher_repository
    try:
        check_duplicate_user(username, email, phone,user_repo)

        logger.debug("Hashing password for user: %s", username)
        hash_password = hasher_repo.hash_password(password)

        user = User(
            id=str(uuid.uuid4()),
            name=name,
            phone=phone,
            email=email,
            username=username,
            hashed_password=hash_password,
            created_at=datetime.now(),
            role=UserRole.MEMBER,
        )
        user_data = Users(**vars(user))
        user_repo.save(user_data)
        logger.info("User created successfully: %s, ID: %s", username, user.id)
        return user
    except Exception as e:
        logger.error("Failed to create user :%s",username)
        raise

def check_duplicate_user(username: str, email: str, phone: str,user_repo:UserRepository) -> bool:

    logger.debug(f"Checking for duplicate user with username: {username}, email: {email}, phone: {phone}")

    if user_repo.get_by_username(username):
        logger.warning("Duplicate user found: Username %s already",username)
        raise DuplicateUserException("Username already Exist")

    if user_repo.get_by_email(email):
        logger.warning("Duplicate user found: email %s already",email)
        raise DuplicateUserException("Email already Exist")

    if user_repo.get_by_phone(phone):
        logger.warning("Duplicate user found: phone %s already",phone)
        raise DuplicateUserException("Phone already Exist")

    return True

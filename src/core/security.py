from typing import Annotated
from fastapi import Depends,Request
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User, UserRole
from fastapi.security import OAuth2PasswordBearer
# from src.core.provider import Provider
from src.core.log_config import logger
# from src.core.dependencies import get_provider


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/signin',scheme_name="JWT")


# def get_current_user(
#         token:Annotated[str,Depends(oauth2_scheme)],
#         provider:Provider=Depends(get_provider)
        
# ):
    
#     token_repo=provider.token_repository
#     user_repo=provider.user_repository
#     username=token_repo.validate_and_decode_token(token).get("sub")
#     raw_user = user_repo.get_by_username(username)
#     if not raw_user:
#         raise UserNotFoundException("User Not Found")
#     user = user_repo.to_dataclass(raw_user,User)
#     return user

def is_admin(user:User):
    logger.debug("Checking whether user is admin")
    if user.role!=UserRole.ADMIN:
        logger.warning("Unauthorize user: %s trying to access",user.username)
        raise InvalidMemberTypeException("Access denied. Admin only.")
    return True

def is_member(user:User):
    logger.debug("Checking whether user is member")
    if user.role!=UserRole.MEMBER:
        logger.warning("Unauthorize user: %s trying to access",user.username)
        raise InvalidMemberTypeException("Access denied. Member only.")
    return True


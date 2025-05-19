from src.modules.user.exceptions import InvalidMemberTypeException
from src.modules.user.entity.user import User, UserRole
from src.core.log_config import logger





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


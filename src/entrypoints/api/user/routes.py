from fastapi import APIRouter, Request
from src.modules.user.application import  user_service
from src.entrypoints.api.user.responses import AllUserResponse,UserIdResponse
from src.core.dependencies import AnnotatedRepositoryProvider,AnnotatedCurrentUser
from src.core.security import is_admin
from src.core.log_config import logger
from src.core.exceptions import UnauthorizedException


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def list_user_resource(
    request: Request,
    provider:AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser,

):
    logger.info("User %s trying to access user list",user.username)
    is_admin(user)
    users = user_service.list_users(provider)
    logger.debug("Retrieved %d users", len(users))
    return [AllUserResponse(**vars(user)) for user in users]



@router.get("/me/")
async def get_self_user_resource(
    request: Request,
    user: AnnotatedCurrentUser,
    provider:AnnotatedRepositoryProvider
):
    logger.info("User %s requested their profile",user.username)
    user = user_service.get_user_by_id(user.id,provider)
    logger.debug("User data retrieved for self user %s", user.id)
    return UserIdResponse(**vars(user))
    



@router.get("/{user_id}")
async def get_user_resource(
    request: Request,
    user_id: str,
    user: AnnotatedCurrentUser,
    provider:AnnotatedRepositoryProvider
):
    logger.info("User %s requested info for user %s", user.id,user_id)
    is_admin(user)
    user = user_service.get_user_by_id(user.id,provider)
    logger.debug("Retrieved data for user %s", user_id)
    return UserIdResponse(**vars(user))
    



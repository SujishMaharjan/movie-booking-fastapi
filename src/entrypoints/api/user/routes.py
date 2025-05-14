from fastapi import APIRouter, Request
from src.modules.user.application import  list_users,get_user
from src.entrypoints.api.user.responses import AllUserResponse,UserIdResponse
from src.core.dependencies import AnnotatedRepositoryProvider,AnnotatedCurrentUser
from src.core.security import is_admin


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def list_user_resource(
    request: Request,
    provider:AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser,

):
    is_admin(user)
    users = list_users.ListUser(provider).execute()
    return [AllUserResponse(**vars(user)) for user in users]
    


@router.get("/me/")
async def get_self_user_resource(
    request: Request,
    user: AnnotatedCurrentUser,
    provider:AnnotatedRepositoryProvider
):
    user = get_user.GetUser(provider).execute(user.id)
    return UserIdResponse(**vars(user))


@router.get("/{user_id}")
async def get_user_resource(
    request: Request,
    user_id: str,
    user: AnnotatedCurrentUser,
    provider:AnnotatedRepositoryProvider
):
    
    is_admin(user)
    user = get_user.GetUser(provider).execute(user_id)
    return UserIdResponse(**vars(user))



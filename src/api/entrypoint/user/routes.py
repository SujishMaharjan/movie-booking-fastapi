from fastapi import APIRouter,Request,Depends
from typing import Annotated
from src.db_schemas.user import Users

from src.api.entrypoint.user import models
from src.modules.auth.handlers import check_duplicate_user,persist_user_to_db,get_user
from src.core.extensions import db_dependency
from src.core.security import hash_password,verify_password,create_access_token
from src.modules.auth.handlers import get_current_user
from src.modules.user.handlers import check_user_member_type
from src.modules.user.handlers import get_users()


router = APIRouter(prefix="/Users",tags=["Users"])

@router.get("/")
#later add param for page_number and page_size
async def list_users(request: Request,current_user:Annotated[Users, Depends(get_current_user)]): 
    check_user_member_type(current_user,"admin")
    users = get_users()
    return users

    


@router.put("/{username}")
async def update_user_details(request: Request,username:str): ...




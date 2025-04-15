from fastapi import APIRouter,Request,Depends
from typing import Annotated
from src.db_schemas.user import Users
from src.core.extensions import db_dependency
from src.api.entrypoint.user import models
from src.modules.auth.handlers import check_duplicate_user,persist_user_to_db,get_user_from_db_by_username
from src.core.extensions import db_dependency
from src.core.security import hash_password,verify_password,create_access_token
from src.modules.auth.handlers import get_current_user
from src.modules.user.handlers import check_user_member_type
from src.modules.user.handlers import get_users,get_user_by_id


router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/")
#later add param for page_number and page_size
async def list_user_resource(request: Request,db:db_dependency,current_user:Annotated[Users, Depends(get_current_user)]): 
    check_user_member_type(current_user,"admin")
    users = get_users(db)
    return users

@router.get("/{user_id}")
#later add param for page_number and page_size
async def get_user_resource(request: Request,db:db_dependency,user_id:int,current_user:Annotated[Users, Depends(get_current_user)]): 
    check_user_member_type(current_user,"admin")
    users = get_user_by_id(db,user_id)
    return users


# @router.patch("/{user_id}")
# async def update_user_details(request: Request,username:str): ...




from fastapi import APIRouter, Request,Depends
from src.api.entrypoint.reserve import models
from typing import Annotated
from src.modules.auth.handlers import get_current_user
from src.modules.user.handlers import check_user_member_type
from src.modules.reserve.handlers import *
from src.modules.movie.handlers import is_movie_available_to_reserve
from src.db_schemas.user import Users


router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)

@router.get("/")
async def get_reserve_resource(
    request: Request,
    current_user:Annotated[Users, Depends(get_current_user)]):

    logger.info("Reserve endpoint accessed")
    check_user_member_type(current_user,"member")
    reserves = list_reserves_by_user()
    return reserves





@router.post("/")
def create_reserve_resource(
    request: Request,
    model:models.AddReserveModel,
    current_user:Annotated[Users, Depends(get_current_user)]):

    check_user_member_type(current_user,"member")
    is_movie_available_to_reserve(model.movie_name,model.no_of_seats)
    reserve = persist_reserve_to_db(model,current_user)
    return reserve


@router.post("/unreserve")
def unreserve_reserve_resource(
    request: Request,
    model:models.UnReserveModel,
    current_user:Annotated[Users, Depends(get_current_user)]):
    
    check_user_member_type(current_user,"member")
    reserve = check_valid_movie_entered(current_user,model.movie_name)
    check_valid_seats_entered_to_unreserve(reserve,model.no_of_seats)
    reserve =  persist_unreserve_to_db(model,current_user)
    return reserve



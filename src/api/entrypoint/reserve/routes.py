from fastapi import APIRouter, Request,Depends
from src.api.entrypoint.reserve import models
from typing import Annotated
from src.modules.auth.handlers import get_current_user
from src.modules.user.handlers import check_user_member_type
from src.modules.reserve.handlers import *
from src.modules.movie.handlers import get_movie_available_by_movie_name
from src.db_schemas.user import Users
from src.core.extensions import get_db_session
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)

@router.get("/")
async def get_reserve_resource(
    request: Request,
    db_session:Annotated[Session, Depends(get_db_session)],
    current_user:Annotated[Users, Depends(get_current_user)]):

    logger.info("Reserve endpoint accessed")
    check_user_member_type(current_user,"admin")
    reserves = list_out_all_reserves(db_session)
    return reserves





@router.post("/")
async def create_reserve_resource(
    request: Request,
    model:models.AddReserveModel,
    db_session:Annotated[Session, Depends(get_db_session)],
    current_user:Annotated[Users, Depends(get_current_user)]):

    check_user_member_type(current_user,"member")
    is_movie_available_to_reserve(db_session,model.movie_name,model.no_of_seats)
    reserve = persist_reserve_to_db(db_session,model,current_user)
    return reserve



@router.post("/unreserve")
async def unreserve_reserve_resource(
    request: Request,
    model:models.UnReserveModel,
    db_session:Annotated[Session, Depends(get_db_session)],
    current_user:Annotated[Users, Depends(get_current_user)]):
    
    # breakpoint()
    check_user_member_type(current_user,"member")
    reserve,movie= check_valid_movie_entered(db_session,current_user,model.movie_name)
    check_valid_seats_entered_to_unreserve(reserve,model.no_of_seats)
    reserve_response =  persist_unreserve_to_db(db_session,movie,model.no_of_seats,reserve,current_user)
    return reserve_response




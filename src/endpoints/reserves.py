from fastapi import APIRouter,Depends
from typing import Annotated
from ..log import logger
from ..handlers.reserve_handler import add_reserve,get_all_reserves,unreserve_movie
from ..handlers.user_handler import check_user_member_type
from ..dependencies import db_dependency
from ..exceptions import FailedToReserveError,MemberTypeError
from ..model.reserve import ReserveBase
from ..auth.auth import get_current_user
from ..database.models import Users


router = APIRouter(
    prefix="/reserves",
    tags=["reserves"]
)


@router.post("")
async def reserve_movies(db:db_dependency,reserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("Reserve endpoint accessed")

    reserve_response = add_reserve(db,reserve,current_user)
    if not reserve_response:
        raise FailedToReserveError
    
    return reserve_response


@router.get("")
async def show_reserve(db:db_dependency,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("Reserve endpoint accessed")
    if not check_user_member_type(current_user,"member"):
        raise MemberTypeError
    return get_all_reserves(db,current_user)

  
    

@router.put('/unreserve/')
async def unreserve_movies(db:db_dependency,unreserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("reserves/unreserve endpoint accessed")

    unreserve_response=unreserve_movie(db,unreserve,current_user)
    if not unreserve_movies:
        raise FailToUnreserveError
    
    return unreserve_response
    

    
                        
                        